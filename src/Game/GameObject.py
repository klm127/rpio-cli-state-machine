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
        """
        Decreases self.y

        Should only be called by Map object once move is determined valid, not used directly.

        :param num: y to decrease
        :type num: int
        """
        self.y -= num

    def down(self, num=1):
        """
        Increases self.y

        Should only be called by Map object once move is determined valid, not used directly.

        :param num: y to increase
        :type num: int
        """
        self.y += num

    def left(self, num=1):
        """
        Decreases self.x

        Should only be called by Map object once move is determined valid, not used directly.

        :param num: x to decrease
        :type num: int
        """
        self.x -= num

    def right(self, num=1):
        """
        Increases self.x

        Should only be called by Map object once move is determined valid, not used directly.

        :param num: x to increase
        :type num: int
        """
        self.x += num

    def place(self, display):
        """
        Should be overwritten by extending classes

        Places an appropriate character at an appropriate location on the display.

        :param display: Object holding characters to be displayed
        :type display: src.Game.Map.Display
        """
        pass

    def update(self, state, interval):
        """
        Will be called by a map or display object to update the display character if needed
        Only relevant for animated objects
        To be overwritten by extending classes
        :param state: A state holding info about what to display
        :type state: extends class src.Game.Map.GameStates.Game
        :param interval: The time since the last update
        :type interval: float
        """
        pass


class VisibleObject(GameObject):
    """
    An object visible on the display screen

    :param width: The width of the object
    :type width: int
    :param text: The string to display width characters from left
    :type text: str
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

        :param display: Object holding characters to be displayed
        :type display: src.Game.Map.Display
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


