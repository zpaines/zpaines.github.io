#!/usr/bin/env python
# coding: utf-8

numeric_stats = ['derived_fg', 'derived_ft', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
fantasy_stats = ['d_FG%', 'd_FT%', 'FG%', 'FT%','TRB', 'AST', 'STL', 'BLK', 'TOV', '3P', 'PTS']
negative_stats = ['FTA', 'TOV', 'FGA']

import pandas as pd

arr = pd.read_csv('./season_stats.csv').set_index('Player')

raw_draft_values = pd.read_csv('./draft_values.tsv', sep='\t')
raw_draft_values
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
raw_draft_values['Avg $'] = raw_draft_values['Average'].transform(transform_average)
raw_draft_values = raw_draft_values.set_index('Name')
arr = arr.join(raw_draft_values[['Avg $']])
arr = arr.fillna(0)
arr['TOV'] = -1 * arr['TOV']

import os
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'correlations.json')

arr[fantasy_stats+['Avg $']].corr().to_json(path)
arr['TOV'] = -1 * arr['TOV']

path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'player_stats.json')

arr['Name'] = arr.index
arr[fantasy_stats+['Name','Avg $']].to_json(path, orient='records')

import subprocess
subprocess.check_call('npm install', cwd=os.path.dirname(os.path.realpath(__file__)), shell=True)
subprocess.check_call('npm run build', cwd=os.path.dirname(os.path.realpath(__file__)), shell=True)



