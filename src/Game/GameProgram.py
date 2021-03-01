"""
Handles game loops, key presses, and shutting down.

Holds the active state.

Tells state to update whenever its frame rate time passes
"""

from src.StateMachine import Commands, Program, States
from src.Game import GameStates

from pynput import keyboard
import threading
import time


class GameProgram(Program.Program):
    """
    Extends program, adding looping threads that call GameState.update()

    Also reads keyboard input with pynput. Sends key presses to program.execute()
    """
    def __init__(self, display):
        Program.Program.__init__(self)
        self.keyListener = keyboard.Listener(
            on_press=GameProgram.on_key_cb(self, 'press'),
            on_release=GameProgram.on_key_cb(self, 'release')
        )
        self.state = GameStates.Game(self, display)
        self.running = True
        self.frame_rate = 0.05
        self.keyListener.start()
        self.game_thread = threading.Thread(target=GameProgram.get_game_thread_cb(self), daemon=False)
        self.game_thread.start()

    def update(self, interval):
        """
        Called by game thread, just calls update on self.state.
        """
        self.state.update(interval)

    @staticmethod
    def get_game_thread_cb(game_program):
        """
        Callback to get a game thread.

        Returns a function to attach to a game thread. Game thread should not be a daemon.
        The game thread loops while program.running is true.
        If the time since last update exceeds program.frame_rate, thread calls program.update(time interval).

        :param game_program: calling GameProgram
        :type game_program: class GameProgram
        :returns: A function for threading.Thread(target=...)
        :rtype: Function

        """
        def cb():
            last = time.time()
            while game_program.running:
                now = time.time()
                interval = now-last
                if interval >= game_program.frame_rate:
                    game_program.update(interval)
                    last = now

        return cb

    def end_program(self):
        """
        Ends the program by closing threads.
        """
        self.state.end_state()
        self.running = False
        self.game_thread.join()
        self.keyListener.stop()
        exit()

    @staticmethod
    def on_key_cb(program, key_type):
        """
        return callback passed to pynput keyboard listener.

        Builds a dictionary based on key presses / releases and sends
        that dictionary to program.execute when a key press is read.

        Called twice, once to get a callback for key presses, once to
        get a callback for key releases.

        :param program: Program where key presses are read.
        :type program: class GameProgram
        :param key_type: Either 'press' or 'release'
        :type key_type: str
        :returns: A callback to pass to keyboard.Listener of pynput
        :rtype: Function
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
            program.execute(ev)

        return cb
