# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 16:41:43 2022

@author: Seldon
"""

import os 
import pandas as pd
from pathlib import Path
from itertools import chain
from helper import read_yml
from ai_constants import pricing_dict

file_paths_to_translate = ['C:\\Program Files (x86)\\Steam\\steamapps\\common\\Victoria 3\\game\\localization\\english']
def translate_localization(prompt,file_paths_to_translate='all',model='fixthis',generate_bool=False):
    
    # first find files to modify. If directory is given, modify all files within directory

    
    if type(file_paths_to_translate) != list:
        raise ValueError("file_paths must be a list")
        
    ## convert file_paths to Path
    file_paths = [Path(file_path) for file_path in file_paths_to_translate]
    ##  find all files
    file_paths=[file_path.glob('**/*') for file_path in file_paths]
    file_paths = [[x for x in item if x.is_file()] for item in file_paths]
    # flatten list
    file_paths = list(chain(*file_paths))
    
    # https://openai.com/api/pricing/
    # estimate number of tokens needed, as well as pricing per model
    # token estimate is .75* words
    
    
    combined_df = pd.DataFrame()
    for file_path in file_paths:
        df,header = read_yml(file_path)
        df['file_path'] = str(file_path)
        combined_df = pd.concat([combined_df,df])
        
    # calculate number of tokens
    total_words = sum([len(item) for item in combined_df.text.str.split(' ')])
    # note, this is not accounting for prompt
    total_tokens = int(total_words * 4/3)
    
    # calculate pricing
    print("Estimated number of tokens: " + '{:,}'.format(total_tokens))
    for key,val in pricing_dict.items():
        cost = (val/1000)*total_tokens
        txt = "Using model: " + str(key) + " would cost ${cost:.2f}"
        print(txt.format(cost=cost))
        
    # use selects model, then it runs a test case
        
        
        
        
        
        
        
        
        