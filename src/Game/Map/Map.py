"""
Holds the game map, whether win has been reached, or whether a lose condition has been triggered.

Handles `MapObjects` that desire to move.
"""
from src.Game.Map import Tile, DisplayObject, Player


class Map:
    """
    The game map.

    Holds a 2D array of `MapSquare` objects.
    """
    def __init__(self, map_array, player_x, player_y):
        self.mapArray = map_array  # an array of map objects.
        self.moveRequests = []  # current move requests
        self.height = len(self.mapArray)
        self.width = len(self.mapArray[0])
        self.player = Player.Player(player_x, player_y, self)
        self.win_reached = False
        self.lose = False

    def get_square(self, x, y):
        """
        Gets the mapSquare object at x,y
        :param x: x coordinate of map square
        :type x: int
        :param y: y coordinate of map square
        :type y: int
        """
        if x < 0 or x > self.width-1 or y < 0 or y > self.height-1:
            return MapSquare(x, y, Tile.Wall, '~')  # return a wall if at end of map
        return self.mapArray[y][x]

    def get_display_object(self, x, y):
        """
        Gets the display object at a square, for use by Viewport class
        :param x: x-coordinate of map square
        :type x: int
        :param y: y-coordinate of map square
        :type y: int
        """
        if x < 0 or x >= self.width:
            return DisplayObject.StaticObject(chr(0b11110111))
        if y < 0 or y >= self.height:
            return DisplayObject.StaticObject(chr(0b11110111))
        return self.mapArray[y][x].get_display_object()

    def request_move(self, map_object, x, y):
        """
        Called by a movable game object when it wants to move. Adds move to an array for processing.

        :param map_object: A Map Object
        :type map_object: class MapObject
        :param x: desired new x
        :type x: int
        :param y: desired new y
        :type y: int
        """
        self.moveRequests.append([map_object, x, y])

    def process_moves(self):
        while len(self.moveRequests) > 0:
            m = self.moveRequests.pop()  # m[0]=object, m[1]=new x, m[2]=new y
            target_square = self.get_square(m[1], m[2])
            if target_square.collide(m[0]):
                old_square = self.get_square(m[0].x, m[0].y)
                i = old_square.objects.index(m[0])
                old_square.objects.pop(i)
                target_square.objects.append(m[0])
                m[0].x = m[1]
                m[0].y = m[2]
            m[0].viewport.load_view()
            m[0].moving = False


class MapSquare:
    """
    A map square.

    Holds its x and y value, a MapTile object, and an object

    If object is equal to 0, there is no object.

    Passed the actual class of Tile, not a tile instance. Initializes Tile itself.

    :param x: The x-coordinate on the map this square exists
    :param y: The y-coordinate on the map this square exists
    :param tile_class: A tile to initialize on the square
    :type tile_class: class Class extends Map.Tile
    """
    def __init__(self, x, y, tile_class, character):
        self.x = x
        self.y = y
        self.tile = tile_class(character)
        self.objects = []

    def collide(self, map_object):
        """
        Called by Map object when a Map Object tries to move into tihs Map Square.
        Checks if anything in this square makes it not passable. If not passable, returns False

        :param map_object: The object attempting to move into this square.
        :type map_object: MapObject
        """
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
        """
        Gets the appropriate object for rendering on a Display.

        Will be the tile if there are no objects in the square.

        Otherwise, will be the topmost object.
        """
        if len(self.objects) == 0:
            return self.tile.get_display_object()
        else:
            return self.objects[-1].get_display_object()
