"""
A Game object. Holds x and y positions
"""


class GameObject:
    """
    A game object holding position and size info.

    x,y are top left coordinates for variable size object

    :param x: the x coordinates on the game map
    :type x: int
    :param y: the y coordinates on the game map
    :type y: int
    :param width: the width
    :type width: int
    """
    def __init__(self, x, y, width=1):
        self.x = x
        self.y = y
        self.width = width

    def up(self, num=1):
        self.y -= num

    def down(self, num=1):
        self.y += num

    def left(self, num=1):
        self.x -= num

    def right(self, num=1):
        self.x += num

    def place(self, display):
        pass

    def update(self, state, interval):
        pass


class VisibleObject(GameObject):
    """
    An object visible on the display screen

    :param width: The width of the object
    :type width: int
    :param string: The string to display width characters from left
    :type string: str
    :param x: the x coordinate of object
    :type x: int
    :param y: the y coordinate of object
    :type y: int
    """
    def __init__(self, x, y, width=1, text=','):
        GameObject.__init__(self, x, y, width)
        self.text = text

    def place(self, display):
        """
        Sets characters on display to correspond with this object
        """
        for i in range(0, self.width):
            if i < len(self.text):
                display.change(self.y, self.x + i, self.text[i])


class AnimatedObject(VisibleObject):
    """
    Extends visible object with a method to change visible character

    Parent class, not to be used directly.

    :param x: the x-coordinate
    :type x: int
    :param y: the y-coordinate
    :type y: int
    :param interval: interval between animation changes
    :type interval: float
    """
    def __init__(self, x, y, width, interval, string=','):
        VisibleObject.__init__(self, x, y, width, string)
        self.interval = interval
        self.time_since_last = 0

    def update(self, state, interval):
        """
        Checks if the interval calls for a change in this object

        :param state: state where object exists
        :type state: class GameState
        :param interval: time elapsed
        :type interval: float
        """
        self.place(state.display)
        self.time_since_last += interval
        change_amount = int(self.time_since_last / self.interval)
        self.time_since_last -= self.interval * change_amount
        self.change(state, change_amount)

    def change(self, state, amount):
        """
        Method to be overwritten.

        Changes the object in some way if the interval has passed.
        """
        pass


