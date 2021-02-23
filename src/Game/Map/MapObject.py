"""
For objects on the map

Not a tile; an object that may be placed on a tile.
"""


class MapObject:
    def __init__(self, passable):
        self.passable = passable

    def collide(self, map_object):
        pass

    def get_display_object(self):
        pass


class Lava(MapObject):
    def __init__(self, passable):
        MapObject.__init__(self, passable)

    def collide(self, map_object):
        map_object.destroy()


class WinZone(MapObject):
    def __init__(self, passable):
        MapObject.__init__(self, passable)
