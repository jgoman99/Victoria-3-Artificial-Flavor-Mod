# Victoria 3 Artificial Flavor Mod

This is a project to add flavor to Victoria 3 using OpenAI.

## Country Description Flavor

For the english localization:
Country tags:
Victoria 3\game\localization\english\countries_l_english.yml
Country descriptions:
Victoria 3\game\localization\english\country_flavor_text_l_english.yml

First, we load country tags information, then we extract country tag (e.g. USA) with country name (e.g. United State of America)
Second, we now create a dataframe with the columns being country tag, country name
Third, we load country descriptions file, and extract country descriptions by tag and add them to the dataframe
Fourth, we discard generic country descriptions and replace with blanks
Fifth, we save dataframe as .csv
Sixth we extract a subset of the country descriptions that are not blank, and use them to create the training data for open ai
Seventh, we run open ai's fine tune. This allows us to simplify our queries
Eighth, we run fine tuned model on country names
Ninth, we output result as .yml