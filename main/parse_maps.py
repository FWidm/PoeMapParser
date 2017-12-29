import json

import marshmallow
from PyPoE.poe.file.dat import RelationalReader
from PyPoE.poe.file.ggpk import GGPKFile

from main.models import Map
from main.schemas.MapSchema import MapSchema
#todo: comments, refactor

def load_ggpk(ggpk_path):
    """
    Creates a ggpk object from a path
    :param ggpk_path:
    :return: ggpk
    """
    ggpk = GGPKFile()
    ggpk.read(ggpk_path)
    ggpk.directory_build()
    return ggpk


def create_relational_reader(ggpk):
    """
    Create a relational reader object that reads from the given ggpk
    :param ggpk: ggpk object
    :return: relationalreader instance
    """
    opt = {
        'use_dat_value': False,
        'auto_build_index': True,
    }
    return RelationalReader(path_or_ggpk=ggpk, read_options=opt, raise_error_on_missing_relation=False)


def safe_init(r, key):
    try:
        obj = r[key]
    except:
        print("Exception")
        obj = r[key]
    return obj


def parse(r: RelationalReader):
    maps = safe_init(r, "Maps.dat")
    base_items = safe_init(r, 'BaseItemTypes.dat')
    # print(r.__dict__)
    maps.build_index('Regular_WorldAreasKey')
    maps.build_index('Unique_WorldAreasKey')

    mapDictList = []
    index = 0
    for node in r['AtlasNode.dat']:
        index = index + 1
        map = maps.index['Regular_WorldAreasKey'].get(node['WorldAreasKey'])
        unique = False
        if map is None:
            map = maps.index['Unique_WorldAreasKey'].get(node['WorldAreasKey'])
            unique = True
        if map is None:
            print('Missing: %s' % node['WorldAreasKey']['Id'])
            continue
        # indexing creates a list unless unique is specified for the field in the specification
        map = map[0]
        print("{}".format(map['BaseItemTypesKey']['Name']))

        # Pack info
        monster_pack_info = []
        for pack in map['MonsterPacksKeys']:
            pack_dict = {}
            pack_dict['Id'] = pack['Id']
            pack_dict['Tags'] = []
            #get tags
            for tag in pack['TagsKeys']:
                pack_dict['Tags'].append(tag['Id'])

            monster_pack_info.append(pack_dict)

        # Map upgrades into...
        upgrade = None if map['MapUpgrade_BaseItemTypesKey'] == None else \
        base_items[map['MapUpgrade_BaseItemTypesKey'].rowid]['Name']


        # Map is connected to the following higher tier maps
        higher_maps = map['HigherTierMaps_BaseItemTypesKeys']
        connected = []
        for higher_map in higher_maps:
            connected_dict = {}
            connected_dict['Name'] = base_items[higher_map.rowid]['Name']
            # connectedDict['Id'] = None
            connected.append(connected_dict)

        # Map Bosses todo -> Bosses_MonstervarietiesKey -> MonsterVarieties.dat -> Name ...
        boss_list=[]
        for boss in node['WorldAreasKey']['Bosses_MonsterVarietiesKeys']:
            dict ={}
            dict['Name']=boss['Name']
            boss_list.append(dict)

        # Mobs todo -> Monsters_MonstervarietiesKey -> MonsterVarieties.dat -> Name ...
        coordinates={
            "x":node['X'],
            "y":node['Y'],
        }
        map = Map(node['WorldAreasKey']['Name'], map['BaseItemTypesKey']['Name'], map['Tier'], map['Regular_GuildCharacter'], upgrade, connected, boss_list, coordinates,
                  monster_packs=monster_pack_info,unique=unique,flavour_text=node['FlavourText'])
        mapDictList.append(map)

    return mapDictList


path = 'D:/Grinding Gear Games/Path of Exile/Content.ggpk'

print("Loading")
ggpk = load_ggpk(path)
print("Finish")
rr = create_relational_reader(ggpk)
maps=parse(rr)

schema = MapSchema(exclude=['monster_packs'])

#write to file
with open('maps_3_1.json', 'w') as outfile:
    json.dump(schema.dump(maps,many=True).data,outfile,indent=4)
