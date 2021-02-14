#!/usr/bin/env python
# coding: utf-8

# In[1]:

numeric_stats = ['d_FG%', 'd_FT%', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
fantasy_stats = ['d_FG%', 'd_FT%','TRB', 'AST', 'STL', 'BLK', 'TOV', '3P', 'PTS']
negative_stats = ['FTA', 'TOV', 'FGA']

import pandas as pd

arr = pd.read_csv('./season_stats.csv').set_index('Player')

# In[4]:


# Import average draft values TSV
raw_draft_values = pd.read_csv('./draft_values.tsv', sep='\t')
def transform_name(name):
    notes_loc = name.find('Notes')
    if notes_loc > -1:
        name = name[notes_loc+5:]
    note_loc = name.find('Note')
    if note_loc > -1:
        name = name[note_loc+4:]
    names = name.split()
    ret = names[0:2]
    if (names[2] == 'Jr.' or names[2] == 'Sr.'):
        ret = names[0:3]
    return ' '.join(ret)

def transform_average(val):
    val = val[1:]
    try:
        num_val = float(val)
        return num_val
    except ValueError:
        return 0

raw_draft_values['Name'] = raw_draft_values['Name'].transform(transform_name)
raw_draft_values['Average'] = raw_draft_values['Average'].transform(transform_average)
raw_draft_values = raw_draft_values.set_index('Name')
arr = arr.join(raw_draft_values[['Average']])


# In[5]:


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


# In[6]:


z_scores['zach_points'] = z_scores[fantasy_stats].sum(axis=1)
z_scores = z_scores[z_scores.Average != 0]
z_scores['points_per_dollar'] = (z_scores['zach_points'])/z_scores['Average']
top_players = z_scores.nlargest(200, 'zach_points')[fantasy_stats+['zach_points', 'Average', 'points_per_dollar']]


# In[7]:


top_players['Name'] = top_players.index


# In[8]:
import os
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'player_data.json')
top_players.to_json(path_or_buf=path, orient='index')


import subprocess
subprocess.check_call('npm run build', cwd=os.path.dirname(os.path.realpath(__file__)), shell=True)