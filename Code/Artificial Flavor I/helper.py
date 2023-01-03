# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 23:47:28 2022

@author: Seldon
"""
import pandas as pd
import re
import numpy as np
import openai

from ai_constants import models_dict,tokens_dict


# ADDENDUM TO COMMENT BELOW
# API call packing to some degree may be necessary, as their server does not like frequent calls
# so does increase speed, and them not kicking us out

# TOP LEVEL COMMENT
# Optimizing OPENAI prompt (e.g. making sure API call returns close to max tokens)
# is not worth it. AI creativity declines quickly around the 10-20th response.
# I believe this is because davinci gets into a spiral 
# originally it follows your prompt, but as the response gets longer it starts 
# following its own answer to your response more, since it's responses are more vague, it gets confused and becomes more basic, leading to addl replies becoming even more basic
# e.g. first few answers will be 100% what you are looking for
# next few will be 90%, then 80% and so on.

# here we want to set up a smart openai call for the same prompt, basically to minimize cost
# same prompt
# estimate length of responses
# takes input strings, calculates how best to bundle them together,
# use davinci here

def estimate_words(text):
    text = text.replace("\n"," ")
    text = text.replace("  ", " ")
    return(len(text.split(' ')))

# fine tuning
# use prompt text to get training data
# manually use their tools
# fine tune model

# davinci breaks down on large prompts. Do not optimize here, either fine tune, or run with prompt and one completion.
# def generate_prompt_for_style_transfer(prompt,model, string_series):
#     """e.g. prompt = 'write the following in the style of Shakespeare' """
#     target_words = int(tokens_dict[model]*3/4)
#     prompt_words = estimate_words(prompt)
    
#     # add one to simulate adding 1. in front of each prompt
#     series = string_series.apply(estimate_words)
#     # multiply by 1/2 as we want completion text to have space
#     last_string_index = np.where(series.cumsum() < (target_words - prompt_words)*2/5)[0][-1]


#     prompt_text = prompt + ":\n"
#     for num, item in enumerate(string_series.tolist()[0:last_string_index]):
#         prompt_text += str(num+1) + ". " + item + "\n"
        
#     return(prompt_text)

# PROMPT GENERATION FIX
def generate_prompt_for_style_transfer(prompt, string):
    prompt_text = prompt + ":\n" + string
    return(prompt_text)

# TRANSLATE FIX
def get_openai_response_optimized_for_style_transfer(prompt,model,temperature=.5):
    prompt_tokens_est = int(len(prompt.split(' '))*(4/3)*1.25)
    response = openai.Completion.create(
      model=models_dict[model],
      prompt=prompt,
      # change this to change how sure AI is about it's response, 0 is most accurate, 1 is least
      temperature=temperature,
      # Controls max length of response. 
      max_tokens=prompt_tokens_est*4
      #stop = "\n"
    
    )
    return(response)


# this is primarily optimized for davinci
def get_openai_response(prompt,model,temperature=.5):
    prompt_tokens_est = int(len(prompt.split(' '))*(4/3)*1.25)
    response = openai.Completion.create(
      model=models_dict[model],
      prompt=prompt,
      # change this to change how sure AI is about it's response, 0 is most accurate, 1 is least
      temperature=temperature,
      # Controls max length of response. 
      max_tokens=3500
      #stop = "\n"
    
    )
    return(response)

# combines generate prompt with open ai response


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