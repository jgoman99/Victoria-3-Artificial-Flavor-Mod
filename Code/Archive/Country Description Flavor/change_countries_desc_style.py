# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 23:47:05 2022

@author: Seldon
"""

import openai
import numpy as np
from helper import reformat_countries_desc_to_df, convert_countries_flavor_df_to_countries_flavor_yml

def get_new_style_country_desc(country_desc,style_string):
    """
    function to generate country descriptions based on prompt and time string.
    I recommend keeping length of country list below 40. Over 40 and the AI may exceed its
    max response limit.
    
    style_string can be easily modified to change the style of countries description
    """
            
    # create prompt text to send to API
    prompt_text = style_string +": " + "'" + str(country_desc) + "'"
            
    response = openai.Completion.create(
      # Model used. davinci is the most versatile model, so we will use that.
      # It is also the most expensive.
      model="text-davinci-003",
      prompt=prompt_text,
      # change this to change how sure AI is about it's response, 0 is most accurate
      temperature=.9,
      # Controls max length of response. 
      max_tokens=100,
      #stop = "\n"
    
    )
    
    return(response)

def change_countries_desc_style(countries_tag_path,countries_flavor_text_path, \
                            new_countries_flavor_text_path,style_string='Change the style to pirate speech'):
    """
    change_countries_desc_style uses openai's API to change the style of existing country flavor text.
    
    :param countries_tag_path: country localization file, e.g. "common\Victoria 3\game\localization\english\countries_l_english.yml"
    :param countries_flavor_text_path: country flavor localization file, e.g. "common\Victoria 3\game\localization\english\country_flavor_text_l_english.yml"
    :param new_countries_flavor_text_path: where you want to output the new country description
    :param style_string: modify this to change style, e.g. "to cockney english"
    """
    
    countries_df = reformat_countries_desc_to_df(countries_tag_path,countries_flavor_text_path)
    countries_df = countries_df[countries_df.country_orig_desc.notna()]
    
    countries_df['country_ai_desc'] = np.nan
    num_obs = countries_df.shape[0]
    count = 0
    for idx, row in countries_df.iterrows():
        count+=1
        print("processing: " +str(count/num_obs))
        country_desc = row.country_orig_desc
        response = get_new_style_country_desc(country_desc,style_string)
        countries_df.loc[idx,'country_ai_desc'] = response['choices'][0]['text'].replace("\n\n","")
        
    convert_countries_flavor_df_to_countries_flavor_yml(countries_df,new_countries_flavor_text_path)
    
    
    
    
    
    
    
    
    
    
    