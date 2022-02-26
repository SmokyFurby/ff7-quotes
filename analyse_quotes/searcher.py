import pandas as pd
import os
from analyse_quotes.config import WORKING_DIR
from analyse_quotes.utils import read_txt_lines

csv_file = "FF7quotes.csv"
csv_path = os.path.join(WORKING_DIR, "data", csv_file)

df = pd.read_csv(csv_path, index_col=None)

heroes_txt_path = os.path.join(WORKING_DIR, "input_files", 'heroes.txt')
words_txt_path = os.path.join(WORKING_DIR, "input_files", 'words.txt')

heroes = read_txt_lines(heroes_txt_path)
words = read_txt_lines(words_txt_path)

for word in words:
    tally = {
        hero: df[
            df['name'].str.contains(hero) & df['quote'].str.contains(word, na=False)
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
