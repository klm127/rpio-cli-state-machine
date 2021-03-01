"""
Floors and Walls

Each may or may not be passable and has a display object.

Part of Map.MapSquare; each MapSquare can have only 1 Tile
"""
from src.Game.Map import DisplayObject


class Tile:
    """
    A general tile, passable.

    :param char: The character displayed if no objects also in MapSquare. Default E
    :type char: char
    """
    def __init__(self, char='E'):
        self.char = char
        self.passable = True
        self.display_object = DisplayObject.StaticObject(char)

    def get_display_object(self):
        return self.display_object


class Floor(Tile):
    """
    A floor tile, passable.

    :param character: The char to display. Default ':'
    :type character: char
    """
    def __init__(self, character=':'):
        Tile.__init__(self, char=character)


class Wall(Tile):
    """
    A wall tile, impassable

    :param character: The char to display. Default 'X'
    :type character: char
    """
    def __init__(self, character='X'):
        Tile.__init__(self, char=character)
        self.passable = False
