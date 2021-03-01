"""
The starting state for the game.

Shows some text and spinners to introduce the player to the game.

When space-bar is pressed or when the text is finished scrolling, loads up the MapState to begin game.

Extends src.Game.Map.GameStates.Game

"""

from src.Game.GameStates import Game
from src.Game import TitleScreenObjects

from src.StateMachine.Commands import Command

from src.Game.MapState import MapState


class GameStart(Game):
    def __init__(self, program, display):
        Game.__init__(self, program, display)
        self.game_objects.append(TitleScreenObjects.TextScroll("Game Time!!!", 0.3))
        wave_num = 1
        wave_rising = True
        for i in range(0, 16):
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

    def done(self, scroll_text):
        """
        Called by the instances of TextScroll in TitleScreenObjects.

        Lets this state know that the text scrolls are done scrolling.

        GameStart looks at which text scroll is done, then creates the next one.

        :param scroll_text: The calling scroll text object
        :type scroll_text: class src.Game.Map.TitleScreenObjects.TextScroll
        """
        if scroll_text.text == "Game Time!!!":
            self.game_objects.append(TitleScreenObjects.TextScroll("You are a one-eyed pirate! " + chr(1)+chr(2)))
        elif scroll_text.text == "You are a one-eyed pirate! " + chr(1) + chr(2):
            self.game_objects.append(TitleScreenObjects.TextScroll("Fumble through the maze! "))

    @staticmethod
    def wave_generator(x, num):
        """
        Returns new instances of `TitleScreenObjects.spinner` to rotate some characters that give the
        vague appearance of being waves, in keeping with the pirate theme.

        :param x: The x on the display, either 1 or 2, to place them (they all start at y=1)
        :type x: int
        :param num: The interval time between frame changes
        :type num: float
        """
        if num == 1:
            return TitleScreenObjects.Spinner(x, 1, ['^', '-', '.', '-'], 1)
        elif num == 2:
            return TitleScreenObjects.Spinner(x, 1, ['-', '.', '-', '^'], 1)
        elif num == 3:
            return TitleScreenObjects.Spinner(x, 1, ['.', '-', '^', '-'], 1)
        elif num == 4:
            return TitleScreenObjects.Spinner(x, 1, ['-', '^', '-', '.'], 1)

    @staticmethod
    def next_state(state, inp):
        """
        Called by a `Command` through an `effect` callback.

        Triggered by space bar on the title screen.

        Sets self.program.state to a `MapState` instance, passing the same display this state used to `MapState`

        Neither parameter is actually used, but this is the structure of a command callback.

        :param state: The calling state (will be self)
        :type state: extends class src.StateMachine.States.State
        :param inp: The input - will be a key dict
        :type inp: dict
        """
        state.program.state = MapState(state.program, state.display)
        state.end_state()

