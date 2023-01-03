# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 18:07:30 2022

@author: Seldon
"""
import pandas as pd
from ai_constants import models_dict
from helper import get_openai_response

# tests

prompt = "Convert the following to pirate speech:\n1: Our architects believe that innovations involving steel frames and concrete would allow the construction of buildings taller than ever conceived before. They urge us to authorize a survey to identify the best possible site to lay the foundations."
models = models_dict.values()
response_list = []
for model in models:
    print('model')
    response = get_openai_response(prompt,model)
    response_list.append(response)
    
response_df=pd.DataFrame({'model' : models, 'response' : [response['choices'][0]['text'] for response in response_list]})
