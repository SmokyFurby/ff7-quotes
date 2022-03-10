"""
Author: Belgin Seymenoglu
Source of in-game text: http://letao.is-a-geek.net
Please do not use this tool or any of its output for commercial gain
"""
import os
from analyse_quotes import config
from analyse_quotes.scraper import scrape_and_save_quotes
from analyse_quotes.swearing.advanced_filter import filter_heroes
from analyse_quotes.swearing.filter_setup import load_quotes

if __name__ == "__main__":
    current_dir = os.getcwd()

    scrape_and_save_quotes(
        current_dir=current_dir,
        cols=config.cols,
        csv_file_name=config.csv_file_name
    )

    quote_df, heroes, _ = load_quotes(
        current_dir=current_dir,
        csv_file=config.csv_file_name
    )

    filter_heroes(
        quote_df=quote_df,
        heroes=heroes
    )

