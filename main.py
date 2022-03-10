import os
import typing

from analyse_quotes import config
from analyse_quotes.scraper import scrape_and_save_quotes
from analyse_quotes.swearing.advanced_filter import filter_heroes
from analyse_quotes.swearing.filter_setup import load_quotes


def scrape_and_analyse(
        column_names: typing.List[str],
        csv_file_name: str
):
    current_dir = os.getcwd()

    scrape_and_save_quotes(
        current_dir=current_dir,
        cols=column_names,
        csv_file_name=csv_file_name
    )

    quote_df, heroes, _ = load_quotes(
        current_dir=current_dir,
        csv_file=csv_file_name
    )

    filter_heroes(
        quote_df=quote_df,
        heroes=heroes
    )


if __name__ == "__main__":
    scrape_and_analyse(
        column_names=config.cols,
        csv_file_name=config.csv_file_name
    )
