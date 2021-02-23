"""
Floors and Walls
"""


class Tile:
    def __init__(self, char = 'E'):
        self.char = char
        self.passable = True

    def get_visible_object(self):
        pass


class Floor(Tile):
    def __init__(self, char = ':'):
        Tile.__init__(self, char)


class Wall(Tile):
    def __init__(self, char = 'X'):
        Tile.__init__(self, char)
        self.passable = False
