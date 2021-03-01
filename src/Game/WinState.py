"""
The state reached when the final level is beaten
"""

from src.Game.GameStates import Game
from src.Game import TitleScreenObjects

from src.StateMachine.Commands import Command


class Win(Game):
    def __init__(self, program, display):
        Game.__init__(self, program, display)
        win = TitleScreenObjects.TextScroll(">VICTORY<", 0.2, 16, 0)
        self.win2 = TitleScreenObjects.TextScroll(">VICTORY<", 0.1, 18, 1)
        self.game_objects.append(win)
        self.game_objects.append(self.win2)
        
    def done(self, scroll_text):
        if scroll_text is self.win2:
            pass
        pass   # add something for clearing the display?
