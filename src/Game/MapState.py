from src.Game.GameStates import Game
from src.Game.Map import Map
from src.StateMachine.Commands import Command
from src.Game.Map import Levels


class MapState(Game):
    def __init__(self, program, display):
        Game.__init__(self, program, display)
        self.Map = Levels.Levels.demo.get_map()
        self.player = self.Map.player
        self.view = self.Map.player.viewport
        self.commands.add(Command(self, Game.is_key_cb("press", "Key.right"), MapState.right_press))
        self.commands.add(Command(self, Game.is_key_cb("press", "Key.left"), MapState.left_press))
        self.commands.add(Command(self, Game.is_key_cb("press", "Key.up"), MapState.up_press))
        self.commands.add(Command(self, Game.is_key_cb("press", "Key.down"), MapState.down_press))

    def update(self, interval):
        """
        Overwritten method
        Then calls display.print to display.
        :param interval: The time since last update.
        :type interval: float
        """
        self.Map.process_moves()
        self.display.blank()
        self.view.load_to_display(self.display)
        self.display.print()

    @staticmethod
    def right_press(state, inp):
        state.player.right_pressed()

    @staticmethod
    def left_press(state, inp):
        state.player.left_pressed()

    @staticmethod
    def up_press(state, inp):
        state.player.up_pressed()

    @staticmethod
    def down_press(state, inp):
        state.player.down_pressed()
