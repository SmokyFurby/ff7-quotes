import typing
import pandas as pd
from profanity_filter import ProfanityFilter


def is_string_profane(
        profanity_filter: ProfanityFilter,
        quote: typing.Optional[str]
):
    """
    Test whether inputted string contains profanities.
    :param profanity_filter: profanity filter
    :param quote: quote to analyse
    :return: boolean indicating whether the quote contains swear words
    """
    if type(quote) == str:
        return profanity_filter.is_profane(quote)
    else:
        return False


def filter_heroes(
        quote_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Group quotes by heroes and analyse their lines using a profanity filter
    :param quote_df: dataframe with quotes and names of the speakers
    :return: dataframe with number of quotes, numebr of swear lines and swear ratio
    """
    # TODO: seek a way to vectorise the profanity filter
    profanity_filter = ProfanityFilter()

    quote_df["is_profane"] = quote_df["quote"].apply(
        lambda x: is_string_profane(profanity_filter, x)
    )

    quotes_by_hero = quote_df.groupby(by=["name"])

    swear_sums = quotes_by_hero.sum()["is_profane"]
    totals = quotes_by_hero.count()["quote"]

    swear_df = pd.concat([swear_sums, totals], axis=1)

    swear_df = swear_df.rename(columns={
        "is_profane": "number_swear_lines",
        "quote": "total_lines_said"
    })

    swear_df["swear_ratio"] = swear_df["number_swear_lines"] / swear_df["total_lines_said"]

    return swear_df
