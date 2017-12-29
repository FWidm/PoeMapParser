from main.fetch_map_img import fetch_map_img


class Map:
    def __init__(self, name, base, tier, guild_character, upgrade, connected_to, boss, coordinates, monster_packs=None,
                 unique=False, flavour_text=None):
        super().__init__()
        self.base = base
        self.tier = tier
        self.guild_character = guild_character
        self.unique = unique
        self.upgrade = upgrade
        self.connected_to = connected_to
        self.boss=boss
        self.monster_packs = monster_packs
        self.name = name
        self.coordinates = coordinates
        self.flavour_text=flavour_text
        self.img= self.fetch_img()

    def fetch_img(self):
        return fetch_map_img(self.__dict__,out_path="img")

    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}:'{value}'".format(key=key, value=self.__dict__[key]))

        return ', '.join(sb)

    def __repr__(self):
        return self.__str__()