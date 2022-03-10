import os
import typing
import pandas as pd
from analyse_quotes.utils import read_txt_lines


def load_quotes(
        current_dir: str,
        csv_file: str
) -> typing.Tuple[pd.DataFrame, typing.List[str], typing.List[str]]:
    """
    Load the csv containing scraped quotes
    :param current_dir: psth to current working directory
    :param csv_file: name of csv file containing quotes
    :return: dataframe containing quotes, the list of names of the
    heroes and list of test swear words
    """
    print("Loading quotes.")
    csv_path = os.path.join(current_dir, "data", csv_file)

    df = pd.read_csv(csv_path, index_col=None)

    heroes_txt_path = os.path.join(
        current_dir,
        "input_files",
        "heroes.txt"
    )
    words_txt_path = os.path.join(
        current_dir,
        "input_files",
        "words.txt"
    )

    heroes = read_txt_lines(heroes_txt_path)
    words = read_txt_lines(words_txt_path)

    return df, heroes, words
