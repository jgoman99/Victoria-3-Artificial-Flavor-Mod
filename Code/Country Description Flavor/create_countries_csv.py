# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 16:41:52 2022

@author: Seldon
"""

from pathlib import Path
import pandas as pd
import numpy as np
import re
eng_localization_dir = Path("C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\localization\english")

countries_path = eng_localization_dir /Path("countries_l_english.yml")
countries_flavor_path = eng_localization_dir / Path("country_flavor_text_l_english.yml")
countries_csv_path = Path("countries_desc.csv")
train_path = Path("countries_desc_train.jsonl")
num_samples = 10

with open(countries_path, 'r', encoding ='utf-8') as file:
    countries_lines = file.readlines()
    countries_lines = countries_lines[1:]
    countries_lines = [item.strip() for item in countries_lines]
    countries_lines = [item.replace("\n","") for item in countries_lines]
    countries_lines = [item.replace('"',"") for item in countries_lines]
    countries_lines = [item for item in countries_lines if re.match("[A-Z]{3}\:[0-9]",item)]
    
    country_tuples = [re.split("(?:\:[0-9] )",item) for item in countries_lines]
    
    
country_df = pd.DataFrame(country_tuples,columns = ['country_tag','country_name'])

with open(countries_flavor_path, 'r', encoding ='utf-8') as file:
    countries_flavor_lines = file.readlines()
    countries_flavor_lines = countries_flavor_lines[1:]
    countries_flavor_lines = [item.strip() for item in countries_flavor_lines]
    countries_flavor_lines = [item.replace("\n","") for item in countries_flavor_lines]
    countries_flavor_lines = [item.replace('"',"") for item in countries_flavor_lines]
    countries_flavor_lines = [item for item in countries_flavor_lines if re.match("^[A-Z]{3}",item)]
    country_flavor_tuples  = [re.split("(?:\:[0-9] )",item) for item in countries_flavor_lines]
    
country_flavor_df = pd.DataFrame(country_flavor_tuples,columns = ['country_tag','country_orig_desc'])
country_flavor_df.country_tag = country_flavor_df.country_tag.str.replace("_FLAVOR_TEXT","")
country_flavor_df.loc[country_flavor_df.country_orig_desc.str.contains("\$"),"country_orig_desc"] = np.nan


country_df = pd.merge(country_df,country_flavor_df, how = 'left')
country_df.to_csv(countries_csv_path,index=False)

# create training data for openai
train_df = country_df[country_df.country_orig_desc.notna()]
train_df = train_df[['country_name','country_orig_desc']]
train_df.columns = ["prompt","completion"]
train_df.to_json(train_path, orient='records', lines=True)

Prompt: Bavaria 
Response: In the wake of recent revolutions across Europe, Bavaria has turned to reaction. But the embers of rebellion still burn; will Bavaria be consumed by the flames?
Prompt: Belgium
Response: In Belgium the industrial revolution is in full swing. The yoke of Dutch oppression was cast aside just six years ago and the country is bounding ahead of their former masters, with the construction of the first railroad in continental Europe. What does the future hold for them?
Prompt: United States
Response:
