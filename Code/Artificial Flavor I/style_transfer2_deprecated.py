# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 16:41:43 2022

@author: Seldon
"""

from time import sleep
import os 
import pandas as pd
import numpy as np
from pathlib import Path
from itertools import chain
from helper import read_yml, write_yml, get_openai_edit_reponse
from ai_constants import pricing_dict
import re
import random as rd

# Update: OpenAI edit functionality is not mature enough to be useful in this context. (1/3/23)
# NOTE: This file differs from the previous file by using openai's edit model. 
# This model seems more applicable to style transfer, and is currently free (as of 1/3/23)
file_paths_to_translate = ['C:\\Program Files (x86)\\Steam\\steamapps\\common\\Victoria 3\\game\\localization\\english\\ai_strategies_l_english.yml']

instruction = 'convert to spanish.'
mod_directory = "../../Mods/Pirate-Theme'd AI Strategies"
temperature = .8
def translate_localization(instruction,file_paths_to_translate,mod_directory,temperature = .5):
    
    # first find files to modify. If directory is given, modify all files within directory
    if type(file_paths_to_translate) != list:
        raise ValueError("file_paths_to_translate must be a list")
        
    ## convert file_paths to Path
    paths = [Path(file_path) for file_path in file_paths_to_translate]
    # for all dirs, find all files
    dirs = [file_path for file_path in paths if file_path.is_dir()]
    files = [file_path for file_path in paths if not file_path.is_dir()]
    ##  find all files
    file_paths=[dir_item.glob('**/*') for dir_item in dirs]
    file_paths = [[x for x in item if x.is_file()] for item in file_paths]
    # flatten list
    file_paths = list(chain(*file_paths))
    file_paths.extend(files)
    
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
    total_tokens = int(total_words * 4/3)
    
    # calculate number of tokens
    # it should be free yay! 
    print("Estimated number of tokens: " + '{:,}'.format(total_tokens))
    print("Pricing for edits is free as of 1/3/23. This may change in the future. Check first before running this script.")

    # create original text column
    combined_df['orig_text'] = combined_df['text']
    # set text to nan
    combined_df['text'] = np.nan
    # use selects model, then it runs a few test cases
    test_bool = True
    while test_bool:
        print("Running Test Samples")
        for idx,row in combined_df.iloc[0:3].iterrows():
            response = get_openai_edit_reponse(row['orig_text'],instruction,temperature)
            combined_df.loc[idx,'text'] = response['choices'][0]['text'].replace('\n','')
            
        for idx, row in combined_df.iloc[0:3].iterrows():
            print('original: ' + str(row['orig_text']))
            print('AI generated: ' + str(row['text']))
            
        deny_bool = True
        while deny_bool:
            user_denies = input("Are the test samples acceptable? Press 'y' to run instruction on everything, 'n' to change instruction")
            if user_denies == 'n':
                instruction = input("Please enter new instruction, e.g. 'convert to charles dickens style of writing'")
                deny_bool = False
            elif user_denies == 'y':
                test_bool = False
                deny_bool = False
                
    # run on everything else
    # try added due to server issues
    count = 0
    for i in range(100):
      for attempt in range(100):
        try:
            for idx,row in combined_df[combined_df.text.isna()].iterrows():
                sleep(rd.randrange(3,4)/10)
                count += 1
                if count % 20 == 0:
                    print('Processing: ' + str(count/combined_df.shape[0]))
                    
                response = get_openai_edit_reponse(row['orig_text'],instruction,temperature)
                combined_df.loc[idx,'text'] = response['choices'][0]['text'].replace('\n','')
                
                print('original: ' + str(combined_df.loc[idx,'orig_text'] ))
                print('AI generated: ' + str(combined_df.loc[idx,'text'] ))
        except Exception as e:
            print("Error message: " + str(e) + ". Retrying")
            sleep(rd.randrange(61,63))
        else:
          break
      else:
        raise ValueError("Something went wrong. It may be server issues")

    # convert to yml, and create new folders
    mod_paths = [Path(item) for item in combined_df['file_path'].unique()]
    # this is a quick method to mod path, it is not good code
    vic3_location =re.findall(".*Victoria 3.*game",str(mod_paths[0]))[0]
    for mod_path in mod_paths:
        new_mod_path = Path(str(mod_path).replace(vic3_location,mod_directory))
        new_mod_path.parent.mkdir(parents=True, exist_ok=True)
        df = combined_df[combined_df['file_path']==str(mod_path)]
        write_yml(df,header,new_mod_path)
    
        

        
        
        
        
        
        
        
        