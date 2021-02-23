"""
The starting state for the game
"""

from src.Game import GameStates
from src.Game import GameObject


class GameStart(GameStates.Game):
    def __init__(self, program):
        GameStates.Game.__init__(self, program)
        self.game_objects.append(GameObject.TextScroll("Game Time!!!"))
        self.game_objects.append(GameObject.Spinner(1, 1, ['x', 'X', 'x', '*']))
        self.game_objects.append(GameObject.Spinner(26, 1, [')', '(', '%']))
        self.game_objects.append(GameObject.Spinner(22, 1, ['_', '-', '^']))
