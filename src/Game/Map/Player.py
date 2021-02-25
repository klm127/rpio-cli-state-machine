"""
The player
"""

from src.Game.Map import DisplayObject, MapObject


class Player(MapObject.MapObject):
    def __init__(self, x, y, game_map):
        MapObject.MapObject.__init__(self, passable=False)
        self.display_object = DisplayObject.StaticObject('@')
        self.x = x
        self.y = y
        self.up_down = "down"
        self.left_right = "right"
        self.char = "@"
        self.game_map = game_map
        game_map.mapArray[y][x].objects.append(self)
        self.viewport = Viewport(self)

    def get_view(self):
        return self.viewport

    def up_pressed(self):
        if self.up_down == "down":
            self.up_down = "up"
        else:
            self.game_map.request_move(self, self.x, self.y-1)
        self.viewport.load_view()

    def down_pressed(self):
        if self.up_down == "up":
            self.up_down = "down"
        else:
            self.game_map.request_move(self, self.x, self.y+1)
        self.viewport.load_view()

    def left_pressed(self):
        if self.left_right == "right":
            self.left_right = "left"
        else:
            self.game_map.request_move(self, self.x-1, self.y)
        self.viewport.load_view()

    def right_pressed(self):
        if self.left_right == "left":
            self.left_right = "right"
        else:
            self.game_map.request_move(self, self.x+1, self.y)
        self.viewport.load_view()


class Viewport:
    def __init__(self, player):
        self.width = 16  # change depending on display parameters
        self.height = 2
        self.player = player
        self.display_array = []
        self.load_view()

    def load_view(self):
        top_row = 0
        start_x = 0
        if self.player.up_down == "down":
            top_row = self.player.y
            # player y start, player y + 1 end
            if self.player.left_right == "right":
                start_x = self.player.x - 7
                # player x - 7 start, player x + 8 end
                pass
            else:  # left
                start_x = self.player.x - 8
                # player x - 8 start, player x + 7 end
                pass
        else:  # up
            top_row = self.player.y - 1
            # player y-1 start, player y + 1 end
            if self.player.left_right == "right":
                start_x = self.player.x - 7
                # player x - 7 start, player x + 8 end
                pass
            else:  # left
                start_x = self.player.x - 8
                # player x - 8 start, player x + 7 end
                pass

        self.display_array = []
        for y in range(0, 2):
            row = []
            for x in range(0, 16):
                row.append(self.player.game_map.get_display_object(x + start_x, y+top_row))
            self.display_array.append(row)

    def load_to_display(self, display):
        for y in range(0,2):
            for x in range(0,16):
                display.change(y, x, self.display_array[y][x].char)

        """
        Loads the display object from the characters viewport to the display
        """

    def update(self):
        """
        will be used to update animated objects.
        """
        pass
