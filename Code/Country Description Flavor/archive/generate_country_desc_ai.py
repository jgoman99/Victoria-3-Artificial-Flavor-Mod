# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 18:23:11 2022

@author: Seldon
"""

import pandas as pd
import openai

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

def get_country_desc(country):
    prompt_text = " " + str(country) + " ->"
    response = openai.Completion.create(
      model="davinci:ft-personal-2022-12-24-06-56-18",
      prompt=prompt_text,
      # change this to change how sure AI is about it's response, 0 is most accurate
      temperature=0,
      max_tokens=64,
      stop = "\n"
    
    )
    
    return(response['choices'][0]['text'])


countries_df = pd.read_csv("countries_desc.csv")

# sample_df = countries_df[countries_df.country_orig_desc.notna()].sample(10)
# sample_df['country_ai_desc'] = ""
# for idx, row in sample_df.iterrows():
#     country = row.country_name
#     sample_df.loc[idx,'country_ai_desc'] = get_country_desc(country)
    
# sample_df.to_csv("sample_countries_desc.csv",index=False)

# sample_df2 = countries_df[countries_df.country_orig_desc.isna()].sample(10)
# sample_df2['country_ai_desc'] = ""
# for idx, row in sample_df2.iterrows():
#     country = row.country_name
#     sample_df2.loc[idx,'country_ai_desc'] = get_country_desc(country)
    
# sample_df2.to_csv("sample_countries2_tolerance0_desc.csv",index=False)