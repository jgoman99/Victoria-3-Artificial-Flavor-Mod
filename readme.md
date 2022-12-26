# Victoria 3 Artificial Flavor Mod

This is a project to add flavor to Victoria 3 using OpenAI.

## Code Structure:
code that does stuff
examples - have the form (example.py)

## Country Description Flavor
For the english localization:
Country tags:

Victoria 3\game\localization\english\countries_l_english.yml

Country descriptions:

Victoria 3\game\localization\english\country_flavor_text_l_english.yml

### Quality
Have you ever played a total war game? The descriptions of the factions are often very historically innaccurate, sometimes hilariously.

The AI generated descriptions here for Victoria 3, can be hilarious, e.g. some country's description says located in Africa, but it is actually in Oceania.

However, these are mostly edge cases, for countries/regions where little is known / where paradox has simplified the region into one tag, instead of the many nations
residing there. For more well-known countries, the results are at paradox level generally, and in some cases fairly brilliant, with a level of detail that is fascinating.


### Creation 
1. Load country tags, load country descriptions, create crosswalk. create fine tuned openai's davinci model. The results were mediocre. Add picture
2. Use prompt based approach. Worked. No fine-tuning necessary, cost $1, half of which was due to testing. Results are pretty good.

### Possible Issues
* issue with yml so using readlines instead. I did not pay attention to :0 vs :1. Which could cause problems?


### Todo:
1. Refactor code, add disclaimer to ai part?
2. reword things
3. write scribble with approach used
4. upload to steam workshop
5. figure out other mods to make - maybe dynamic country names? - dynamic names shouldn't be too hard, look at examples of their dynamism to properly go about it,
real question is can I also get the code for the triggers at the same time?
6. May write a read paradox yaml script
7. todo: add option to add true localization e.g. make pirate show up