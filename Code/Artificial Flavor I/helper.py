# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 23:47:28 2022

@author: Seldon
"""
import pandas as pd
import re
import numpy as np
import openai

# here we want to set up a smart openai call for the same prompt, basically to minimize cost

# at some point should load entire localization dir, and check if this parses correctly

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
    # remove quotes from text
    lines = [re.sub('"(?!")',"",line) for line in lines]
    # text
    lines = [re.split('\:(?=[0-9]{1,})',line) for line in lines]
    lines = [[line[0],re.findall("^[0-9]{1,}",line[1])[0],re.findall(" .*",line[1])[0].strip()] \
              for line in lines]

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