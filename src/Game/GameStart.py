"""
The starting state for the game
"""

from src.Game.GameStates import Game
from src.Game import TitleScreenObjects

from src.StateMachine.Commands import Command


class GameStart(Game):
    def __init__(self, program, display):
        Game.__init__(self, program, display)
        self.game_objects.append(TitleScreenObjects.TextScroll("Game Time!!!", 0.3))
        wave_num = 1
        wave_rising = True
        for i in range(1, 27):
            self.game_objects.append(GameStart.wave_generator(i, wave_num))
            if wave_num == 4:
                wave_rising = False
            if wave_num == 1:
                wave_rising = True
            if wave_rising:
                wave_num += 1
            else:
                wave_num -= 1
        self.commands.add(Command(self, Game.is_key_cb("press", "Key.space"), GameStart.next_state))

    @staticmethod
    def wave_generator(x, num):
        if num == 1:
            return TitleScreenObjects.Spinner(x, 1, ['`', '-', '.', '-'], 0.1)
        elif num == 2:
            return TitleScreenObjects.Spinner(x, 1, ['-', '.', '-', '`'], 0.1)
        elif num == 3:
            return TitleScreenObjects.Spinner(x, 1, ['.', '-', '`', '-'], 0.1)
        elif num == 4:
            return TitleScreenObjects.Spinner(x, 1, ['-', '`', '-', '.'], 0.1)

    @staticmethod
    def next_state(state, inp):
        print('next state called in Game Start')
