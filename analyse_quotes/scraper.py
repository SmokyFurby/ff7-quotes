"""
Author: Belgin Seymenoglu
Source of in-game text: http://letao.is-a-geek.net
Please do not use this software or any of its output for commercial gain
"""
import logging
import typing

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

from analyse_quotes.utils import read_txt_lines


def scrape_and_save_quotes(
        current_dir: str,
        cols: typing.List[str]
) -> None:
    """
    Scrape quotes and character names in Final Fantasy 7
    and save as a csv
    :param current_dir: directory to save quotes in
    :param cols: column headers for the csv
    :return: Nothing, just save data to a csv
    """
    # read text file containing names of the nine AVALANCHE members
    heroes_txt_path = os.path.join(current_dir, "input_files", 'heroes.txt')
    urls_txt_path = os.path.join(current_dir, "input_files", 'urls.txt')

    heroes = read_txt_lines(heroes_txt_path)

    # read text file containing list of urls the script is spread across
    urls = read_txt_lines(urls_txt_path)

    df_list = []

    for url in urls:
        df_quotes = scrape_url_and_update_records(
            url=url,
            scrape_delay=3,
            cols=cols,
            heroes=heroes
        )
        df_list.append(df_quotes)

    df_final = pd.concat(df_list)

    save_path = os.path.join(current_dir, "data", 'FF7quotes.csv')

    # export to CSV
    df_final.to_csv(save_path, index=None)


def scrape_url_and_update_records(
        url: str,
        scrape_delay: int,
        cols: typing.List[str],
        heroes: typing.List[str],
) -> pd.DataFrame:
    """
    Scrape quotes and character names from one URL
    :param url: URL for link being scraped
    :param scrape_delay: time delay between attempts at scraping URL
    :param cols: column headers for the csv
    :param heroes: names of the party members
    :return: dataframe with quotes and name of who said it
    """
    logging.info(f"Scraping quotes from:\n{url}")
    sleep(scrape_delay)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # All the characters' lines can be found in the div with class 'content'
    quote_table = soup.find(class_='content')

    # Search for quotes/thoughts within <table> tags
    # Next step: try <p>, <p class = "b">
    quote_table_items = quote_table.find_all('table')

    # Make a big dataframe of quotes
    df = dataframe_from_quote_table(
        quote_table=quote_table_items,
        cols=cols
    )

    # Remove the colon at the end; I only want the name
    df["name"] = df["name"].str.replace(":", "")

    party_mask = df["name"].isin(heroes)

    return df[party_mask]


def dataframe_from_quote_table(
        quote_table,
        cols: typing.List[str]
) -> pd.DataFrame:
    """
    Convert contents of an HTML table's worth of
    quotes to
    :param quote_table: contents of HTML table with
    quotes and speaker's names
    :param cols: column headers for the csv
    :return: dataframe containing quotes and speaker's name
    """
    df_rows = []

    for quote in quote_table:
        for row in quote.find_all('tr'):
            columns = row.find_all('td')
            column_check = [
                columns[0].find('p', class_="n d"),
                columns[1].find('p', class_="d")
            ]
            if column_check == [None, None]:
                new_row = [column.get_text() for column in columns]
                df_row = pd.DataFrame([new_row], columns=cols)
                df_rows.append(df_row)

    logging.info(f"Number of new rows: {len(df_rows)}")
    if len(df_rows) > 0:
        return pd.concat(df_rows)
    else:
        return pd.DataFrame(columns=cols)
