import typing

import pandas as pd
from profanity_filter import ProfanityFilter


def is_string_profane(
        pf,
        quote
):
    if type(quote) == str:
        return pf.is_profane(quote)
    else:
        return False


def filter_heroes(
        quote_df: pd.DataFrame,
        heroes: typing.List[str]
):
    pf = ProfanityFilter()

    quote_df["is_profane"] = quote_df["quote"].apply(
        lambda x: is_string_profane(pf, x)
    )

    for hero in heroes:
        print(f"# {hero}")
        character_lines = quote_df[quote_df.name == hero]

        number_swear_lines = len(
            character_lines[character_lines.is_profane]
        )

        swear_ratio = number_swear_lines / len(character_lines)

        print(f"They swore {number_swear_lines} times in the game")
        print(f"Swear ratio: {swear_ratio}")
