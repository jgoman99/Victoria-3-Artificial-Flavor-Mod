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
        
        
# improved option to read paradox yml files
# some issues with reading may remain
def read_yml(path):
    with open(path, 'r', encoding ='utf-8') as f:
        lines = f.read()
        
    lines = lines.split("\n")
    # skips header
    header = lines[0]
    lines = lines[1:]
    # trim white space
    lines = [line.strip() for line in lines]
    # remove empty lines
    lines = [line for line in lines if line !=""]
    # remove comments lines
    lines = [line for line in lines if line[0] != '#']
    # text 
    lines = [re.split('(?=")',line) for line in lines]
    # this seems janky, may be issues here, will need to bug test
    lines = [[line[0].split(":")[0], line[0].split(":")[1].strip(),line[1]] for line in lines]

    # remove quotes from text
    lines = [[line[0], line[1], line[2].replace('"','')] for line in lines]
    # convert to dataframe
    
    df = pd.DataFrame(lines,columns = ["var","num","text"])
    return(df,header)

def write_yml(df,header,path):
    L = []
    L.append(header)
    L.append("\n")
    for idx,row in df.iterrows():
         line = " " + str(row['var']) + ":" + str(row['num']) + ' "' + str(row['text']) + '"\n'
         L.append(line)
         
    with open(path,"w",encoding='utf-8') as f:
        f.writelines(L)