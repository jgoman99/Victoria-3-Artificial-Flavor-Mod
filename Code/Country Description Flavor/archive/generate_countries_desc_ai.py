# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:23:11 2022

@author: Seldon
"""

import pandas as pd
import openai
import numpy as np
import re
import pickle


# load openai_api_key
# PATH TO YOUR KEY HERE
openai_key_path = "../../Keys/openai.txt"
with open(openai_key_path) as f:
    openai.api_key = f.readlines()[0]

# models
# We have stopped using these in favor of the prompt based solution.
# full sample
# davinci:ft-personal-2022-12-24-03-40-25
# smaller handpicked sample (2)
# does not work at all lol
# davinci:ft-personal-2022-12-24-06-56-18

# generate country flavor descriptions
def get_country_desc(country_list,time_string='in the early 19th century'):
    
    # Loads prompt. It probably should be placed outside the function
    # as we only need to load this once
    with open("prompt.txt") as f:
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
# Note: There may be a bug here, I believe I fixed it, but have not verified
def generate_countries_desc(countries_csv_path,time_string):
    # load countries
    countries_df = pd.read_csv(countries_csv_path)
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
        print(i)
        response = get_country_desc(country_split,time_string)
        response_list.append(response)
    # pickle response for bug testing
    with open('country_ai_desc.pickle', 'wb') as handle:
        pickle.dump(response_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    # process response
    ai_countries_desc_list = \
        [itemy for sublist in [item['choices'][0]['text'].split("\n\n") for item in response_list] for itemy in sublist if itemy !='']

    countries_df['country_ai_desc'] = ai_countries_desc_list
    countries_df.to_csv(countries_csv_path,index=False)
