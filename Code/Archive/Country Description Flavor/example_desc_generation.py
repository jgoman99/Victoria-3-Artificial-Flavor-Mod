# -*- coding: utf-8 -*-
"""
Created on Sun Dec 25 23:35:20 2022

@author: Seldon
"""

from generate_countries_desc import generate_countries_desc
from pathlib import Path
import os
import openai

# change to your openai api key
openai_key_path = "../../Keys/openai.txt"
with open(openai_key_path) as f:
    openai.api_key = f.readlines()[0]


eng_localization_dir = Path("C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\localization\english")
countries_tag_path = eng_localization_dir /Path("countries_l_english.yml")
countries_flavor_text_path = eng_localization_dir / Path("country_flavor_text_l_english.yml")
new_countries_flavor_text_path = "../../Country Description Flavor/localization/english/country_flavor_text_l_english.yml"

generate_countries_desc(countries_tag_path, countries_flavor_text_path, new_countries_flavor_text_path,time_string='in the early 19th century')