import requests
from bs4 import BeautifulSoup
import pandas as pd
from functools import reduce
from time import sleep

"""
Author: Belgin Seymenoglu
Source of in-game text: http://letao.is-a-geek.net
Please do not use this software or any of its output for commercial gain
"""

WORKING_DIR='/Users/belgin/Dropbox/PythonPractice/scrapers/FF7quotes/'

#read text file containing names of the nine AVALANCHE members
heroes = open(WORKING_DIR+'heroes.txt').read().splitlines()
#read text file containing list of urls the script is spread across
urls=open(WORKING_DIR+'urls.txt').read().splitlines()

cols=["name","quote"]
df_final=pd.DataFrame(columns=cols)

for url in urls:
    sleep(3)
    page=requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')

    #All the characters' lines can be found in the div with class 'content'
    quote_table=soup.find(class_='content')

    #Search for quotes/thoughts within <table> tags
    #Next step: try <p>, <p class = "b">
    quote_table_items1=quote_table.find_all('table')

    #Make a big dataframe of quotes
    df = pd.DataFrame(columns=cols)
    #Construct each row of the dataframe
    for quote in quote_table_items1:
        table=quote
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            column_check = [columns[0].find('p',class_="n d"), columns[1].find('p',class_="d")]
            if column_check == [None, None]:
                new_row = [column.get_text() for column in columns]
                df_row = pd.DataFrame([new_row],columns=cols)
                df = df.append(df_row)

    #Remove the colon at the end; I only want the name
    df["name"]=df["name"].str.replace(":", "")

    #How to filter for just one character
    cr_name=[ df["name"].str.contains(heroes[i]) for i in range(len(heroes))]
    criteria = reduce(lambda x, y: x | y, cr_name)
    #cr2=df["quote"].str.contains("broad")
    df_new=df[criteria]
    
    #print(df_new.shape[0])
    df_final=pd.concat([df_final, df_new])

#export to CSV
df_final.to_csv(current_dir+'FF7quotes1.csv',index=None)

# Attempt at checking lines with the 'p' tab. Didn't work well; comment it out for now
#quote_table_items2=quote_table.find_all('p')
#for quote in quote_table_items2:
#    print(quote.prettify())


