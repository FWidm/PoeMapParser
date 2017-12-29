from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from main.models import Map


class MapSchema(Schema):
    base = fields.String()
    name = fields.String()
    tier = fields.Int()
    guild_character = fields.String()
    unique = fields.Boolean()
    upgrade = fields.String()
    connected_to = fields.List(fields.Dict())
    monster_packs = fields.Dict()
    flavour_text = fields.String()
    boss = fields.List(fields.Dict())
    coordinates = fields.Dict()
    img = fields.String()
    class Meta:
           ordered = True

    @post_load
    def make_map(self, data):
        return Map(**data)