"""
For objects on the map

Not a tile; an object that may be placed on a tile.
"""

from src.Game.Map import DisplayObject


class MapObject:
    def __init__(self, passable):
        self.passable = passable
        self.display_object = DisplayObject.StaticObject('.')

    def collide(self, map_object):
        pass

    def get_display_object(self):
        return self.display_object


class Lava(MapObject):
    def __init__(self, passable):
        MapObject.__init__(self, passable)
        self.display_object = DisplayObject.StaticObject('&')

    def collide(self, map_object):
        map_object.destroy()


class WinZone(MapObject):
    def __init__(self, passable):
        MapObject.__init__(self, passable)
        self.display_object = DisplayObject.StaticObject('W')
