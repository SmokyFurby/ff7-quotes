import analyse_quotes.config as config
from analyse_quotes.swearing.filter_setup import load_quotes

quote_df, heroes, words = load_quotes(
    current_dir=config.current_dir,
    csv_file="FF7quotes.csv"
)

for word in words:
    tally = {
        hero: quote_df[
            quote_df['name'].str.contains(hero) & quote_df['quote'].str.contains(word, na=False)
        ].shape[0]
        for hero
        in heroes
    }
    tally = {
        item: tally[item]
        for item
        in tally
        if tally[item] > 0
    }
    print(word)
    print(tally)
