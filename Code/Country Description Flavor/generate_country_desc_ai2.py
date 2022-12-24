# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:23:11 2022

@author: Seldon
"""

import pandas as pd
import openai
import numpy as np
import re
# we can probably increase speed by bundling into one api call.

openai_key_path = "../../Keys/openai.txt"
with open(openai_key_path) as f:
    openai.api_key = f.readlines()[0]

# models
# full sample
# davinci:ft-personal-2022-12-24-03-40-25
# smaller handpicked sample (2)
# does not work at all lol
# davinci:ft-personal-2022-12-24-06-56-18

# we can probably do 40 countries at once
# we can add accuracy thing here
def get_country_desc(country_list):
    with open("prompt2.txt") as f:
        prompt_text = f.readlines()
        
    prompt_text = ''.join(prompt_text) + \
        ', '.join(country_list) + \
            ' in the early 19th century'
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt_text,
      # change this to change how sure AI is about it's response, 0 is most accurate
      temperature=.9,
      max_tokens=3500,
      #stop = "\n"
    
    )
    
    return(response)

# countries_df = pd.read_csv("countries_desc.csv")

# country_list = countries_df.country_name.tolist()
# country_splits = np.array_split(country_list,int(len(country_list)/30))
# ai_country_desc_list = []
# i = 0
# for country_split in country_splits:
#     i+=1
#     print(i)
#     response = get_country_desc(country_split)
#     ai_country_desc = response['choices'][0]['text'].split("\n\n")[1:]
#     ai_country_desc = [re.sub(".*: ","",item) for item in ai_country_desc]
#     ai_country_desc_list.extend(ai_country_desc)
    

# countries_df['country_ai_desc'] = ai_country_desc_list
# countries_df.to_csv("countries_desc_ai.csv",index=False)


