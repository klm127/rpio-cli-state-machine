"""
Game State

Holds a list of game objects. Updates them when program tells state to update
as looping continues.

Handles keyboard input commands as sent by GameProgram.
"""

from src.StateMachine import Commands, Program, States
from src.Game import Display

Command = Commands.Command


class Game(States.State):
    """
    Parent game state.

    Updates game objects and holds commands to change features of state.
    """
    def __init__(self, program, display):
        States.State.__init__(self, program)
        program.verbose = False
        self.game_objects = []
        self.display = display
        self.commands.add(Command(self, Game.is_key_cb('press', 'q'), Game.end_game))

    def update(self, interval):
        """
        Called by game thread.

        Blanks display, then calls update on each game object.
        Then calls display.print to display.
        :param interval: The time since last update.
        :type interval: float
        """
        self.display.blank()
        for o in self.game_objects:
            o.update(self, interval)
        self.display.print()

    """
    Calls end_program on state.program, shutting down all threads and ending the program.
    """
    @staticmethod
    def end_game(state, inp):
        state.program.end_program()

    @staticmethod
    def is_key_cb(key_type, key):
        """
        Callback for use with Command.

        Pass return function to bool_func parameter on Command creation.

        Sees if key has been pressed

        :param key_type: 'press' or 'release'
        :type key_type: str
        :param key: The key to look for
        :type key: str
        """
        def cb(state, inp):
            if inp['type'] == key_type and inp['name'] == key:
                return True
            else:
                return False
        return cb

    @staticmethod
    def print_key_info(state, inp):
        """
        Debug method for Command callbacks.

        Prints the key pressed.

        :param state: Calling state, passed by Command
        :type state: class State
        :param inp: input
        :type inp: dict
        """
        print('Correct key press detected')
        print(inp['name'])

    def end_state(self):
        """
        Overwritten method

        Calls super().end_state() and stops listening to keyboard input
        """
        super().end_state()
        self.game_objects = []
