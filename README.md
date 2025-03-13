# basic_role_play
A base library to contain all the various needs of a Basic Roleplaying character

The primary class for creating a character sheet is `BasicRoleplayCharacter` in `sheets`. Import and then extend this 
class to create a unique class for your game. Even if you intend to use the Basic Roleplaying rules as is, this is a 
good time saver if you'd like to include a setting specific set of default skills. To do so pass in a dict including 
the following key value pair:
```
"new_skill_defaults": {
    "NEW_SKILL_NAME": {"name": "NEW_SKILL_NAME", "category": "NEW_SKILL_CATEGORY", "chance": NEW_SKILL_CHANCE}
} 
```
Note that this is a dictionary of dictionaries. From there, the individual character's skills can be added in a similar
way using the `skills` key.

Characters can be saved and loaded using the `save_character_to_json` and `load_character_from_json` respectively.
Sample character json files can be found in `tests` -> `test_characters`. Alternatively, you can create a character
by unpacking a dict into the object at initialization, that is with `char = BasicRoleplayCharacter(**char_stats)`.
Excluded values with either method will be given a base default value on initialization.

Normal skills rolls are made from the character object with the `.make_skill_roll` method passing in the name of 
the skill as a keyword argument `skill = SKILL_NAME`. Opposed rolls, characteristic rolls, sanity rolls, etc. are also
supported.

You can roll arbitrary dice with `roll_ndm` or `roll_str`. The first takes the number of dice and size of dice 
separately. The latter takes a string of the form "1d6", "1D8", etc and returns the result and additionally supports
negative values for the dice.