"""
Holds the larger game map
"""
import Tile


class Map:
    """
    The game map.

    Holds a 2D array of `MapSquare` objects.
    """
    def __init__(self):
        self.mapArray = []  # an array of map objects.
        self.moveRequests = []  # current move requests
        for y in range(0, 10):
            row = []
            for x in range(0, 10):
                row.append(MapSquare(x, y, Tile.Floor))
            self.mapArray.append(row)
        self.height = len(self.mapArray)
        self.width = len(self.mapArray[0])

    def get_square(self, x, y):
        return self.mapArray[y][x]


class MapSquare:
    """
    A map square.

    Holds its x and y value, a MapTile object, and an object

    If object is equal to 0, there is no object.
    :param x: The x-coordinate on the map this square exists
    :param y: The y-coordinate on the map this square exists
    :param TileClass: A tile to initialize on the square
    :type TileClass: Class Object
    """
    def __init__(self, x, y, tile_class):
        self.x = x
        self.y = y
        self.tile = tile_class()
        self.objects = []

    def collide(self, map_object):
        if not self.tile.passable:
            return False
        else:
            if len(self.objects) == 0:
                return True
            else:
                for o in self.objects:
                    o.collide(map_object)
                    if not o.passable:
                        return False
                return True

    def get_display_object(self):
        if len(self.objects) == 0:
            return self.tile.get_display_object()
        else:
            return self.objects[-1].get_display_object()