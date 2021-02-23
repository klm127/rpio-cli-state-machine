"""
Objects for the title screen.
"""
from src.Game.GameObject import *


class TextScroll(AnimatedObject):
    """
    Text that scrolls across screen, right to left

    :param text: The text to scroll
    :type text: str
    :param interval: The time between moves
    :type interval: float
    """
    def __init__(self, text, interval=0.5):
        width = len(text)
        x = 28
        y = 0
        AnimatedObject.__init__(self, x, y, width, interval, text)

    def change(self, state, amount):
        """
        Overwrites method of AnimatedObject.

        Moves text left if interval has passed.

        :param state: The game state
        :type state: GameState
        :param amount: The number of changes that have occurred
        :type amount: int
        """
        self.left(amount)
        if self.x + self.width < 0:
            try:
                i = state.game_objects.index(self)
                state.game_objects.pop(i)
            except ValueError:
                print("tried to remove a game element not in list!")


class Spinner(AnimatedObject):
    """
    An object that cycles through different characters
    :param x: The x coordinate
    :type x: int
    :param y: The y coordinate
    :type y: int
    :param chars: the characters to cycle through
    :type chars: List<char>
    :param interval: how long between changing character
    :type interval: float
    """
    def __init__(self, x, y, chars, interval=0.2):
        VisibleObject.__init__(self, x, y, 1, chars[0])
        self.chars = chars
        self.index = 0
        self.time_since_last = 0
        self.interval = interval

    def change(self, state, amount):
        new_frame = self.index + amount
        if new_frame >= len(self.chars):
            self.index = len(self.chars) % new_frame
        else:
            self.index = new_frame
        self.string = self.chars[self.index]

