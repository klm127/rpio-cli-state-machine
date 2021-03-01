"""
Game Over state
"""

from src.Game.GameStates import Game
from src.Game import TitleScreenObjects

from src.StateMachine.Commands import Command


class Lose(Game):
    def __init__(self, program, display):
        Game.__init__(self, program, display)
        lose = TitleScreenObjects.TextScroll(">Game Over<", 0.2, 16, 0)
        self.lose2 = TitleScreenObjects.TextScroll(">Sorry<", 0.1, 18, 1)
        self.game_objects.append(lose)
        self.game_objects.append(self.lose2)

    def done(self, scroll_text):
        if scroll_text is self.lose2:
            pass
        pass  # add something for clearing the display?
