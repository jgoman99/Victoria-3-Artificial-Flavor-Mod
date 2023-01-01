# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 00:23:38 2022

@author: Seldon
"""

from change_countries_desc_style import change_countries_desc_style
from pathlib import Path

# Note: You will need to set your openai api key in the enviroment
# e.g. os['OPENAI_API_KEY'] = 'af sgd t4rg'

eng_localization_dir = Path("C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\localization\english")
countries_tag_path = eng_localization_dir /Path("countries_l_english.yml")
countries_flavor_text_path = eng_localization_dir / Path("country_flavor_text_l_english.yml")
new_countries_flavor_text_path = "../../Country Description Flavor/localization/pirate/country_flavor_text_l_pirate.yml"

change_countries_desc_style(countries_tag_path,countries_flavor_text_path, \
                            new_countries_flavor_text_path,style_string='Change the style to pirate speech')