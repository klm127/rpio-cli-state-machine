"""
The player
"""

import MapObject


class Player(MapObject):
    def __init__(self, x, y, game_map):
        MapObject.__init__(self, passable=False)
        self.x = x
        self.y = y
        self.up_down = "down"
        self.left_right = "right"
        self.char = "@"
        self.game_map = game_map
        self.viewport = Viewport(self)

    def get_view(self):
        return self.viewport


class Viewport:
    def __init__(self, player):
        self.width = 28  # change depending on display parameters
        self.height = 2
        self.player = player
        self.display_array = []
        self.load_view()

    def load_view(self):
        if self.player.up_down == "down":
            if self.player.left_right == "right":
                pass
            else:  # left
                pass
        else:  # down
            if self.player.left_right == "right":
                pass
            else:  # left
                pass

    def update(self):
        pass
