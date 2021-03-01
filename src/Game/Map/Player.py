"""
The player
"""

from src.Game.Map import DisplayObject, MapObject


class Player(MapObject.MapObject):
    """
    Contains x,y coordinates on the map for the player.

    Depending on whether self.up_down is "down" or "up" and
    whether self.left_right is "right" or "left", self.viewport
    will load different "views" of what the player can see.

    :param x: The player x-coordinate on the map.
    :type x: int
    :param y: Player y-coordinate on the map.
    :type y: int
    :param game_map: The game map
    :type game_map: class Game.Map.Map
    """
    def __init__(self, x, y, game_map):
        MapObject.MapObject.__init__(self, passable=False)
        self.x = x
        self.y = y
        self.up_down = "down"
        self.left_right = "right"
        self.char = '@'
        self.display_object = DisplayObject.StaticObject(self.char)
        self.game_map = game_map
        self.moving = False
        game_map.mapArray[y][x].objects.append(self)
        self.viewport = Viewport(self)

    def get_view(self):
        """
        Gets the viewport for the player. Called by the `MapState` through the `Map`
        to get what needs to be rendered on the `Display`.
        """
        return self.viewport

    def destroy(self):
        """
        Called when player touches lava.

        Sets self.game_map.lose to True, causing gameover screen to display on the
        next state update.
        """
        self.game_map.lose = True

    def up_pressed(self):
        """
        Requests a move from map.

        Callback for a Command effect.
        """
        if self.up_down == "down":
            self.up_down = "up"
            self.viewport.load_view()
        else:
            self.game_map.request_move(self, self.x, self.y-1)
            self.moving = True

    def down_pressed(self):
        """
        Requests a move from map.

        Callback for a Command effect.
        """
        if self.up_down == "up":
            self.up_down = "down"
            self.viewport.load_view()
        else:
            self.game_map.request_move(self, self.x, self.y+1)
            self.moving = True

    def left_pressed(self):
        """
        Requests a move from map.

        Callback for a Command effect.
        """
        if self.left_right == "right":
            self.left_right = "left"
            self.viewport.load_view()
        else:
            self.game_map.request_move(self, self.x-1, self.y)
            self.moving = True

    def right_pressed(self):
        """
        Requests a move from map.

        Callback for a Command effect.
        """
        if self.left_right == "left":
            self.left_right = "right"
            self.viewport.load_view()
        else:
            self.game_map.request_move(self, self.x+1, self.y)
            self.moving = True


class Viewport:
    """
    Assembles a 2x16 array of DisplayObjects based on where the player is
    on the map and which direction they are looking. Iterates through `MapObjects`
    that are visible and gets each `DisplayObject`.

    :param player: The player whose view this is
    :type player: class Player
    """
    def __init__(self, player):
        self.width = 16  # change depending on display parameters
        self.height = 2
        self.player = player
        self.display_array = []
        self.load_view()

    def load_view(self):
        """
        Sets the top row and left x based on the direction the player is facing.

        Then fills self.display_array with `DisplayObjects` for visible `MapObjects`.
        """
        if self.player.up_down == "down":
            top_row = self.player.y
        else:
            top_row = self.player.y - 1
        if self.player.left_right == "right":
            start_x = self.player.x - 7
        else:
            start_x = self.player.x - 8
        self.display_array = []
        for y in range(0, 2):
            row = []
            for x in range(0, 16):
                row.append(self.player.game_map.get_display_object(x + start_x, y+top_row))
            self.display_array.append(row)

    def load_to_display(self, display, interval):
        """
        Loads the array in self.display_array by passing to each `DisplayObject`
        their x-y coordinates and the Display. The DisplayObjects place a character
        on the Display according to their logic. Also updates DisplayObjects with
        the interval that has passed, which may cause some of them to change what
        character they decide to place.

        :param display: The Display object
        :type display: class Display
        :param interval: Time passed since last update
        :type interval: float
        """
        for y in range(0,2):
            for x in range(0,16):
                d_obj = self.display_array[y][x]
                d_obj.update(interval)
                d_obj.display(x, y, display)
                #  display.change(y, x, self.display_array[y][x].char)

        """
        Loads the display object from the characters viewport to the display
        """
