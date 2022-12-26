# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:04:40 2022

@author: Seldon
"""

from pathlib import Path
import pandas as pd
import numpy as np

def convert_csv_to_yml(countries_csv_path,mod_path):
    countries_df = pd.read_csv(countries_csv_path)
    countries_df.country_desc = countries_df.country_ai_desc.replace(np.nan,"No description generated.")
    # convert to desc
    
    L = []
    L.append('\ufeffl_english:\n')
    for idx,row in countries_df.iterrows():
         line = " " + str(row.country_tag) + "_FLAVOR_TEXT:0 " + '"' + str(row.country_ai_desc) + '"' + "\n"
         L.append(line)
         
    with open(mod_path,"w",encoding='utf-8') as f:
        f.writelines(L)