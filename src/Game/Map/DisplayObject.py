"""
For displaying game objects such as `Map.Tile` and `Map.MapObject`.

Similar to `src.Game.GameObject` (and may be merged eventually) but does not hold x and y coordinates.

Instead, x y coordinates are given to instance of `DisplayObject` at the time the object is displayed by the Map

MapObjects hold instances of `DisplayObject` that they return when its time for them to be displayed.

Essentially, information about how something on the map should appear on the display.
"""


class StaticObject:
    def __init__(self, char):
        self.char = char

    def display(self, x, y, display):
        """
        Changes the display at row y column x to self.char.

        :param x: the x-coordinate of the display to change
        :type x: int
        :param y: the y-coordinate of the display to change
        :type y: int
        :param display: the Display to change
        :type display: class src.Game.Display
        """
        display.change(y, x, self.char)

    def update(self, interval):
        pass


class AnimatedObject(StaticObject):
    """
    Extends Static Object
    """
    def __init__(self, chars, interval=0.2):
        self.chars = chars
        self.index = 0
        print(self.chars[0])
        StaticObject.__init__(self, self.chars[0])
        self.interval = interval
        self.time_passed = 0

    def update(self, interval):
        self.time_passed += interval
        if self.time_passed > self.interval:
            self.time_passed = 0
            self.index += 1
            if self.index + 1 > len(self.chars):
                self.index = 0
            self.char = self.chars[self.index]

