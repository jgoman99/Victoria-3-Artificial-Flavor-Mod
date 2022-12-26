# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 16:41:52 2022

@author: Seldon
"""

from pathlib import Path
import pandas as pd
import numpy as np
import re

# read victoria 3 countries yml and output information in csv form
# e.g.
# eng_localization_dir = Path("C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\localization\english")
# countries_path = eng_localization_dir /Path("countries_l_english.yml")
# countries_flavor_path = eng_localization_dir / Path("country_flavor_text_l_english.yml")
# countries_csv_path = Path("countries_desc.csv")
def create_countries_desc_csv(countries_path,countries_flavor_path,countries_csv_path):
    # read countries_l_english.yml
    with open(countries_path, 'r', encoding ='utf-8') as file:
        countries_lines = file.readlines()
        countries_lines = countries_lines[1:]
        countries_lines = [item.strip() for item in countries_lines]
        countries_lines = [item.replace("\n","") for item in countries_lines]
        countries_lines = [item.replace('"',"") for item in countries_lines]
        countries_lines = [item for item in countries_lines if re.match("[A-Z]{3}\:[0-9]",item)]
        
        country_tuples = [re.split("(?:\:[0-9] )",item) for item in countries_lines]
        
    
    # read country_flavor_text_l_english.yml
    with open(countries_flavor_path, 'r', encoding ='utf-8') as file:
        countries_flavor_lines = file.readlines()
        countries_flavor_lines = countries_flavor_lines[1:]
        countries_flavor_lines = [item.strip() for item in countries_flavor_lines]
        countries_flavor_lines = [item.replace("\n","") for item in countries_flavor_lines]
        countries_flavor_lines = [item.replace('"',"") for item in countries_flavor_lines]
        countries_flavor_lines = [item for item in countries_flavor_lines if re.match("^[A-Z]{3}",item)]
        country_flavor_tuples  = [re.split("(?:\:[0-9] )",item) for item in countries_flavor_lines]
       
    # create country dataframe
    country_df = pd.DataFrame(country_tuples,columns = ['country_tag','country_name'])
    # create country flavor dataframe
    country_flavor_df = pd.DataFrame(country_flavor_tuples,columns = ['country_tag','country_orig_desc'])
    country_flavor_df.country_tag = country_flavor_df.country_tag.str.replace("_FLAVOR_TEXT","")
    country_flavor_df.loc[country_flavor_df.country_orig_desc.str.contains("\$"),"country_orig_desc"] = np.nan
    
    # merge
    country_df = pd.merge(country_df,country_flavor_df, how = 'left')
    country_df.to_csv(countries_csv_path,index=False)

