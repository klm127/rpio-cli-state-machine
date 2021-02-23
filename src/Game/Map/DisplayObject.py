"""
For interfacing with GameObjects
"""


class StaticObject:
    def __init__(self, char):
        self.char = char

    def display(self, x, y, display):
        display.change(y, x, self.char)


class AnimatedObject(StaticObject):
    def __init__(self, chars, interval=0.2):
        StaticObject.__init__(chars[0])
        self.interval = interval

