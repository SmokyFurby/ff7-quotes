import os

from analyse_quotes import config
from analyse_quotes.scraper import scrape_and_save_quotes


if __name__ == "__main__":
    current_dir = os.getcwd()
    scrape_and_save_quotes(
        current_dir=current_dir,
        cols=config.cols
    )

