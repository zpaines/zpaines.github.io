#!/usr/bin/env python
# coding: utf-8

# In[1]:


numeric_stats = ['derived_fg', 'derived_ft', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
fantasy_stats = ['FG', 'FGA', 'FTA', 'FT', 'TRB', 'AST', 'STL', 'BLK', 'TOV', '3P', 'PTS']
negative_stats = ['FTA', 'TOV', 'FGA']


# In[2]:


# Import stats CSV
import pandas as pd

arr = pd.read_csv('./season_stats.csv').set_index('Player')


# In[3]:


transform_functions = {}
for col in arr.iteritems():
    stat = col[0]
    if stat in numeric_stats:
        std_dev = arr[stat].std()
        mean = arr[stat].mean()
        if stat in negative_stats:
            std_dev=std_dev*-1
        transform_functions[stat] = lambda val,mean=mean,std_dev=std_dev: (val-mean)*1000/std_dev
    else:
        transform_functions[stat] = lambda val: val
arr = arr.dropna()
z_scores = arr.transform(transform_functions)


# In[4]:


z_scores['zach_points'] = z_scores[fantasy_stats].sum(axis=1)
stats = arr[fantasy_stats+['FT%', 'FG%']].copy()
stats['total_production'] = z_scores['zach_points']


# In[6]:

import os
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'stats.json')
stats.to_json(path_or_buf=path, orient='index')


import subprocess
subprocess.check_call('npm install', cwd=os.path.dirname(os.path.realpath(__file__)), shell=True)
subprocess.check_call('npm run build', cwd=os.path.dirname(os.path.realpath(__file__)), shell=True)

# In[ ]:




