# PoeMapParser
Extract map data from the GGPK into json. Also fetches map images by obtaining the links from poe.ninja.

## Contents
- **fetch_map_img.py**: Given a dictionary that contains the name, tier and unique state of a map, query poe.ninja's api and obtain the image file. method returns the local file path to the img.
    - Required information: current maps (including path to their icons) `abyss_map_url = 'http://poe.ninja/api/Data/GetMapOverview?league=Abyss'` && `abyss_unique_map_url = 'http://poe.ninja/api/Data/GetUniqueMapOverview?league=Abyss'` -- change league to the current league.

- **parse_maps.py**: Given the directory of the GGPK, this extracts various map information from it and creates a json file. Content of the json can be modified by excluding attributes via Marshmallow's `exclude` option.
- **Model & Schema**: Easier adaption of output via Marshmallow

## Output
Example map:
```json
[
...
{
      "base": "Crystal Ore Map",
      "name": "Crystal Ore",
      "tier": 12,
      "guild_character": "\u00e5",
      "unique": false,
      "upgrade": "Caldera Map",
      "connected_to": [
          {
              "Name": "Caldera Map"
          }
      ],
      "flavour_text": "As the torch flickers, brilliance emerges in boundless variance.",
      "boss": [
          {
              "Name": "Lord of the Hollows"
          },
          {
              "Name": "Messenger of the Hollows"
          },
          {
              "Name": "Champion of the Hollows"
          }
      ],
      "coordinates": {
          "y": 287.1709899902344,
          "x": 636.8740234375
      },
      "img": "img/12/Crystal_Ore.png"
  }
...
]
```
