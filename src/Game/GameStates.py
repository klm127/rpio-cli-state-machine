"""
Game Parent State

listens to keyboard inputs
"""

from src.StateMachine import Commands, Program, States
from src.Game import Display
from pynput import keyboard

import time
import threading

Command = Commands.Command


class Game(States.State):
    def __init__(self, program):
        States.State.__init__(self, program)
        program.verbose = False
        self.game_objects = []
        self.display = Display.Display()
        self.keyListener = keyboard.Listener(
            on_press=Game.on_key_cb(self, 'press'),
            on_release=Game.on_key_cb(self, 'release')
        )
        self.running = True
        self.keyListener.start()
        self.game_thread = threading.Thread(target = Game.get_game_thread_cb(self), daemon=False)
        self.game_thread.start()
        self.commands.add(Command(self, Game.is_key_cb('press', 'q'), Game.end_game))

    @staticmethod
    def get_game_thread_cb(state):
        """
        Callback to get game thread

        :param state: calling state
        :type state: class State
        """
        def cb():
            last = time.time()
            while state.running:
                now = time.time()
                if now-last >= 0.4:
                    state.update()
                    last = now
        return cb

    def update(self):
        """
        Called by game thread, updates as needed
        """
        self.display.blank()
        for o in self.game_objects:
            o.update(self)
        self.display.print()

    @staticmethod
    def end_game(state, inp):
        state.running = False
        state.game_thread.join()
        state.end_state()

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
    def on_key_cb(state, key_type):
        """
        return callback passed to pynput keyboard listener

        Not for giving to Command callbacks

        :param state: state context to get execution
        :type state: class State
        :param key_type: Either 'press' or 'release'
        :type key_type: str
        """

        def cb(key):
            key_name = 'none'
            try:
                key_name = key.char
            except AttributeError:
                key_name = str(key)  # Key.left, Key.right, Key.esc etc
            ev = {
                'type': key_type,
                'name': key_name,
            }
            state.program.execute(ev)

        return cb

    @staticmethod
    def print_key_info(state, inp):
        """
        Debug method for Command callbacks
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
        self.keyListener.stop()
