"""
Floors and Walls
"""
from src.Game.Map import DisplayObject


class Tile:
    def __init__(self, char='E'):
        self.char = char
        self.passable = True
        self.display_object = DisplayObject.StaticObject(char)

    def get_display_object(self):
        return self.display_object


class Floor(Tile):
    def __init__(self, character=':'):
        Tile.__init__(self, char=character)


class Wall(Tile):
    def __init__(self, character='X'):
        Tile.__init__(self, char=character)
        self.passable = False
