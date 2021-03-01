"""
Objects on the map.

Not a tile; an object that may be placed on a tile.
"""

from src.Game.Map import DisplayObject


class MapObject:
    """
    General map object, held in an array by a map square which also holds a tile

    Can be passable or not. Has a display object that is returned when it's time to display

    :param passable: whether it can be walked into
    :type passable: boolean
    """
    def __init__(self, passable):
        self.passable = passable
        self.display_object = DisplayObject.StaticObject('.')

    def collide(self, map_object):
        pass

    def get_display_object(self):
        return self.display_object


class Lava(MapObject):
    """
    When this is touched, the colliding object gets .destroy() called on it

    As of this version, the only object that can move is the player and
    touching lava causes player to lose the game.
    """
    alt = 1  # alternates char arrays

    def __init__(self, passable):
        MapObject.__init__(self, passable)
        if Lava.alt == 1:
            self.display_object = DisplayObject.AnimatedObject(['8', 'o'])
            Lava.alt = 2
        else:
            Lava.alt = 1
            self.display_object = DisplayObject.AnimatedObject(['o', '8'])

    def collide(self, map_object):
        """
        Calls .destroy() on the map_object which, as of this iteration, will be the player.

        This in turn sets the lose condition on `Map`, causing GameOver at next update.
        """
        print('touched lava')
        map_object.destroy()


class WinZone(MapObject):

    """
    Colliding with this object causes next level to be loaded by `MapState`

    Otherwise, causes game `WinState` to be loaded
    """
    def __init__(self, passable):
        MapObject.__init__(self, passable)
        self.display_object = DisplayObject.StaticObject('%')

    def collide(self, map_object):
        """
        Called by map when something collides with this
        :param map_object: the colliding object
        :type map_object: class Map.MapObject
        """
        #  check to make sure this is player if I add enemies at some point
        map_object.game_map.win_reached = True
