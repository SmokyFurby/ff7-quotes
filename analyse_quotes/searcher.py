#import modules
import pandas as pd
import os
from os.path import abspath,dirname
import string
import spacy
from spacy.matcher import PhraseMatcher

#Split up sentences into words
nlp=spacy.load('en')
matcher = PhraseMatcher(nlp.vocab, attr='LOWER')

def processing(text):
    doc=nlp(text)
    lemmas=[token.lemma_ for token in doc if token.is_stop==False]
    lemmas=[lemma for lemma in lemmas if lemma !='-PRON-']
    return lemmas

#Turn data from csv into a dataframe
csv_file= '../data/FF7quotes1.csv'
current_dir=os.getcwd()+'/'
csvpath=current_dir+csv_file

df=pd.read_csv(csvpath,index_col=None)

#TODO: ADD THIS IN PROPERLY!
#Split up sentences into words
#df["quote_words"]=df["quote"].str.translate(str.maketrans('','',string.punctuation))
#df["quote_words"]=df["quote_words"].str.lower().str.split()

#df["quote_words"]=processing(df["quote"])
#df=df[df["quote_words"] != []]
df['quote']=df['quote'].str.lower()

hero='Cloud';word='damn';
cr1 = df['name'].str.contains(hero)
cr2 = df['quote'].str.contains(word)

heroes = open(current_dir+'heroes.txt').read().splitlines()
words = open(current_dir+'words.txt').read().splitlines()

for word in words:
    tally={hero:df[
        df['name'].str.contains(hero) & df['quote'].str.contains(word, na=False)].shape[0]
           for hero in heroes}
    tally={item:tally[item] for item in tally if tally[item]>0}
    print(word)
    print(tally)
