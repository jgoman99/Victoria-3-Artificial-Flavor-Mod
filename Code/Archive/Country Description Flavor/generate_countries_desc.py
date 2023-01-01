# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 22:49:22 2022

@author: Seldon
"""

# we will rename this file
import pandas as pd
import re
import numpy as np 
import openai
import pickle
import os
from helper import reformat_countries_desc_to_df, convert_countries_flavor_df_to_countries_flavor_yml



def get_country_desc(country_list,time_string):
    """
    function to generate country descriptions based on prompt and time string.
    I recommend keeping length of country list below 40. Over 40 and the AI may exceed its
    max response limit.
    
    time_string can be easily modified to change countries description to earlier time periods. Be aware that the responses will be better for more well known countries.
    """
    # Loads prompt
    with open("countries_desc_prompt.txt") as f:
        prompt_text = f.readlines()
            
    # create prompt text to send to API
    prompt_text = ''.join(prompt_text) + \
        ', '.join(country_list) + \
            ' ' + time_string
            
    response = openai.Completion.create(
      # Model used. davinci is the most versatile model, so we will use that.
      # It is also the most expensive.
      model="text-davinci-003",
      prompt=prompt_text,
      # change this to change how sure AI is about it's response, 0 is most accurate
      temperature=.9,
      # Controls max length of response. 
      max_tokens=3500,
      #stop = "\n"
    
    )
    
    return(response)



# countries_csv_path = Path("countries_desc.csv")
def generate_countries_desc(countries_tag_path,countries_flavor_text_path, \
                            new_countries_flavor_text_path,time_string='in the early 19th century'):
    """
    generate_countries_desc uses openai's API to generate country flavor text.
    
    :param countries_tag_path: country localization file, e.g. "common\Victoria 3\game\localization\english\countries_l_english.yml"
    :param countries_flavor_text_path: country flavor localization file, e.g. "common\Victoria 3\game\localization\english\country_flavor_text_l_english.yml"
    :param new_countries_flavor_text_path: where you want to output the ai generate country description
    :param time_string: modify this to change time period, e.g. "in the late 1500s"
    """
    # create countries dataframe from yml
    countries_df = reformat_countries_desc_to_df(countries_tag_path,countries_flavor_text_path)
    # convert to list
    country_list = countries_df.country_name.tolist()
    # we can increase speed and reduce number of tokens used by bundling into one api call. Maximum tokens returned is
    # about 4k, so we want to make sure our API calls use as many countries as possible w/o exceeding 4k limit.
    country_splits = np.array_split(country_list,int(len(country_list)/30))
    response_list = []
    i = 0
    # call API
    for country_split in country_splits:
        i+=1
        print("processing: " + str(i/len(country_splits)))
        response = get_country_desc(country_split,time_string)
        response_list.append(response)
    # pickle response for bug testing
    with open('country_ai_desc.pickle', 'wb') as handle:
        pickle.dump(response_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    # process response
    ai_countries_desc_list = \
        [itemy for sublist in [item['choices'][0]['text'][2:].split("\n\n") for item in response_list] for itemy in sublist if itemy !='']

    countries_df['country_ai_desc'] = ai_countries_desc_list
    convert_countries_flavor_df_to_countries_flavor_yml(countries_df,new_countries_flavor_text_path)

