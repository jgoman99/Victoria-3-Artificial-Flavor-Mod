# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 23:47:28 2022

@author: Seldon
"""
import pandas as pd
import re
import numpy as np

def read_countries_tag_yml(countries_tag_path):
    """ function to read countries tag yml"""
    with open(countries_tag_path, 'r', encoding ='utf-8') as file:
        countries_lines = file.readlines()
        
    countries_lines = countries_lines[1:]
    countries_lines = [item.strip() for item in countries_lines]
    countries_lines = [item.replace("\n","") for item in countries_lines]
    countries_lines = [item.replace('"',"") for item in countries_lines]
    countries_lines = [item for item in countries_lines if re.match("[A-Z]{3}\:[0-9]",item)]
    
    country_tuples = [re.split("(?:\:[0-9] )",item) for item in countries_lines]
    
    country_df = pd.DataFrame(country_tuples,columns = ['country_tag','country_name'])
    return(country_df)

def read_countries_flavor_yml(countries_flavor_text_path):
    """ function to read countries flavor text yml"""
    with open(countries_flavor_text_path, 'r', encoding ='utf-8') as file:
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
    
    return(country_flavor_df)

def reformat_countries_desc_to_df(countries_tag_path,countries_flavor_text_path):
    """ function that reads yml and connects countries tags to original name and original country flavor text"""
    country_df = read_countries_tag_yml(countries_tag_path)
    country_flavor_df = read_countries_flavor_yml(countries_flavor_text_path)
    country_df = pd.merge(country_df,country_flavor_df, how = 'left')
    return(country_df)

def convert_countries_flavor_df_to_countries_flavor_yml(countries_df,new_countries_flavor_text_path):
    """ converts countries_df with ai generated responses to yml"""
    countries_df.country_ai_desc = countries_df.country_ai_desc.replace(np.nan,"No description generated.")
    # convert to desc
    
    L = []
    L.append('\ufeffl_english:\n')
    for idx,row in countries_df.iterrows():
         line = " " + str(row.country_tag) + "_FLAVOR_TEXT:0 " + '"' + str(row.country_ai_desc) + '"' + "\n"
         L.append(line)
         
    with open(new_countries_flavor_text_path,"w",encoding='utf-8') as f:
        f.writelines(L)