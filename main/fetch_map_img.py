import json
import os
import re
import urllib.request

import requests
import sys

abyss_map_url = 'http://poe.ninja/api/Data/GetMapOverview?league=Abyss'
abyss_unique_map_url = 'http://poe.ninja/api/Data/GetUniqueMapOverview?league=Abyss'
json_file = 'maps_3_1.json'

poe_ninja_map_data = requests.get(abyss_map_url).json()['lines']
poe_ninja_unique_map_data = requests.get(abyss_unique_map_url).json()['lines']

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    s = str(s).strip().replace('ö', 'oe')
    s = str(s).strip().replace('ä', 'ae')
    s = str(s).strip().replace('ü', 'ue')
    return re.sub(r'(?u)[^-\w.]', '', s)

def fetch_map_img(map, out_path='out'):
    """
    Fetches the image for a given map dictionary. The dictionary must have
    - name: string (see example maps.json for naming info)
    - tier: int
    - unique: bool
    :param map:
    :param out_path:
    :return:
    """
    #fixe the name if the name == The HoGM instead of HoGM to match poe.ninja naming
    name = map['name'] if map['name'] != "The Hall of Grandmasters" else "Hall of Grandmasters"
    icon_url = [x['icon'] for x in poe_ninja_map_data if x['name'].startswith(name + " Map")]
    uniqueIcon = [x['icon'] for x in poe_ninja_unique_map_data if x['name'].startswith(name)]


    if icon_url == []:
        icon_url = uniqueIcon
        if icon_url == []:
            print("Missing: {}".format(name))

    if len(icon_url) == 1:
        path = out_path+"/unique/" if map['unique'] \
            else out_path+"/" + str(map['tier']) + "/"

        if not os.path.exists(path):
            os.makedirs(path)
        try:
            file_name=path + get_valid_filename(map['name']) + ".png"
            url=icon_url[0].replace('scale=1&scaleIndex=0&w=1&h=1&','')
            print(url)
            urllib.request.urlretrieve(url, file_name)
            print("Fetched {}".format(name))
            return file_name
        except:
            print("Name={}, Unexpected error: {}".format(name,sys.exc_info()[0]))
            return None


# maps = json.load(open(json_file))
# img=fetch_map_img(maps[5])
# print(img)
