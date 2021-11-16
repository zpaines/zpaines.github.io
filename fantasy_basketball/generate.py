#!/usr/bin/env python
# coding: utf-8

# In[1]:


numeric_stats = ['derived_fg', 'derived_ft', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
fantasy_stats = ['d_FG%', 'd_FT%', 'FG%', 'FT%','TRB', 'AST', 'STL', 'BLK', 'TOV', '3P', 'PTS']
negative_stats = ['FTA', 'TOV', 'FGA']


# In[2]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.basketball-reference.com/leagues/NBA_2022_totals.html'
r = requests.get(url)
r_html = r.text
soup = BeautifulSoup(r_html,'html.parser')


# In[3]:


table=soup.find_all(class_="full_table")
    
""" Extracting List of column names"""
head=soup.find(class_="thead")
column_names_raw=[head.text for item in head][0]

column_names_polished=column_names_raw.replace("\n",",").split(",")[2:-1]


# In[4]:


players=[]
    
for i in range(len(table)):    
    player_=[]
    for td in table[i].find_all("td"):
        val = td.text
        try:
            val = float(td.text)
        except ValueError:
            pass
        player_.append(val)
    players.append(player_)
    
player_stats=pd.DataFrame(players, columns=column_names_polished)


# In[5]:


import unidecode

def name_transform(name):
    name = name.split('\\')[0].strip()
    name = unidecode.unidecode(name)
    transforms = {}
    transforms['Marcus Morris'] = 'Marcus Morris Sr.'
    transforms['Otto Porter'] = 'Otto Porter Jr.'
    if name in transforms:
        return transforms[name]
    return name
arr = player_stats
arr['Player'] = arr['Player'].transform(name_transform)
arr = arr.drop(['GS', 'Age', 'Pos', 'FG%', 'FT%', '2P%', 'eFG%', '3PA', '3P%', '2P', '2PA', 'Tm'], axis=1)
arr['FT%'] = arr['FT'] * 100 / arr['FTA']
arr['FG%'] = arr['FG'] * 100 / arr['FGA']
arr['d_FG%'] = arr['FG'] * (arr['FG%'] - arr['FG%'].mean())
arr['d_FT%'] = arr['FT'] * (arr['FT%'] - arr['FT%'].mean())
arr[['TRB', 'AST', 'STL', 'BLK', 'TOV', '3P', 'PTS']] = arr[['TRB', 'AST', 'STL', 'BLK', 'TOV', '3P', 'PTS']].div(arr['G'], axis=0)
f = open('./season_stats.csv', 'w')
arr.to_csv(f)
f.close()


import production_vs_cost.generate
import your_league.generate
import correlations.generate



