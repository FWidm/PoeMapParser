import json
from pprint import pprint

import marshmallow
from PyPoE.poe.file.dat import RelationalReader
from PyPoE.poe.file.ggpk import GGPKFile

from main.models import Map
from main.schemas.MapSchema import MapSchema


def load_ggpk(ggpk_path):
    ggpk = GGPKFile()
    ggpk.read(ggpk_path)
    ggpk.directory_build()
    return ggpk


def create_relational_reader(ggpk):
    opt = {
        'use_dat_value': False,
        'auto_build_index': True,
    }
    return RelationalReader(path_or_ggpk=ggpk, read_options=opt, raise_error_on_missing_relation=True)


def safe_init(r, key):
    try:
        obj = r[key]
    except:
        print("Exception")
        obj = r[key]
    return obj


def parse(r: RelationalReader):
    maps = safe_init(r, "Maps.dat")
    monster_packs = safe_init(r, 'MonsterPacks.dat')
    base_items = safe_init(r, 'BaseItemTypes.dat')
    # print(r.__dict__)
    maps.build_index('Regular_WorldAreasKey')
    maps.build_index('Unique_WorldAreasKey')

    mapDictList = []
    index = 0
    for node in r['AtlasNode.dat']:
        index = index + 1
        map = maps.index['Regular_WorldAreasKey'].get(node['WorldAreasKey'].rowid)
        unique = False
        if map is None:
            map = maps.index['Unique_WorldAreasKey'].get(node['WorldAreasKey'].rowid)
            unique = True
        if map is None:
            print('Missing: %s' % node['WorldAreasKey']['Id'])
            continue
        # indexing creates a list unless unique is specified for the field in the specification
        map = map[0]
        print("{}".format(map['BaseItemTypesKey']['Name']))

        # Pack info
        monster_pack_info = {}
        for key in map['MonsterPacksKeys']:
            monster_pack_info['Id'] = monster_packs[key]['Id']
            monster_pack_info['Tags'] = []
            for tag in monster_packs[key]['TagsKeys']:
                monster_pack_info['Tags'].append(tag['Id'])

        # Map upgrades into...
        upgrade = None if map['MapUpgrade_BaseItemTypesKey'] == None else \
        base_items[map['MapUpgrade_BaseItemTypesKey']]['Name']


        # Map is connected to the following higher tier maps
        higher_maps = map['HigherTierMaps_BaseItemTypesKeys']
        connected = []
        for higher_map in higher_maps:
            connectedDict = {}
            connectedDict['Name'] = base_items[higher_map]['Name']
            print("--{}".format(base_items[higher_map]['Name']))
            # connectedDict['Id'] = None
            connected.append(connectedDict)

        # Map Bosses todo

        map = Map(map['BaseItemTypesKey']['Name'], map['Tier'], map['Regular_GuildCharacter'], upgrade, connected,
                  monster_pack_info, node['WorldAreasKey']['Name'], unique)
        print(map.__dict__)
        mapDictList.append(map)
    return mapDictList


path = 'D:/Grinding Gear Games/Path of Exile/Content.ggpk'

print("Loading")
ggpk = load_ggpk(path)
print("Finish")
rr = create_relational_reader(ggpk)
maps=parse(rr)

schema = MapSchema()

with open('maps_3_1.json', 'w') as outfile:
    json.dump(schema.dump(maps,many=True).data,outfile,indent=4)
