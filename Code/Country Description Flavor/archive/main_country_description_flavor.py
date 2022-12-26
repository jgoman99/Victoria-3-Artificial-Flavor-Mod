# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 19:30:35 2022

@author: Seldon
"""

from pathlib import Path
from create_countries_csv import create_countries_desc_csv
from generate_countries_desc_ai import generate_countries_desc
from convert_countries_csv_to_yml import convert_csv_to_yml

eng_localization_dir = Path("C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game\localization\english")
countries_path = eng_localization_dir /Path("countries_l_english.yml")
countries_flavor_path = eng_localization_dir / Path("country_flavor_text_l_english.yml")
countries_csv_path = Path("countries_desc.csv")

create_countries_desc_csv(countries_path,countries_flavor_path,
                          countries_csv_path)
generate_countries_desc(countries_csv_path,time_string='in the early 19th century')

countries_flavor_mod_path = Path("../../Country Description Flavor/localization/english/country_flavor_text_l_english.yml")
convert_csv_to_yml(countries_csv_path,countries_flavor_mod_path)

