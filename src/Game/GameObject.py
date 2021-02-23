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
    :param height: the height
    :type height: int
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
        self.x -= 1

    def right(self, num=1):
        self.x += 1

    def place(self, display):
        pass

    def update(self, state):
        pass


class VisibleObject(GameObject):
    """
    An object visible on the display screen

    :param x: the x coordinate of object
    :type x: int
    :param y: the y coordinate of object
    :type y: int
    """
    def __init__(self, x, y, width=1, string='x'):
        GameObject.__init__(self, x, y, width)
        self.string = string

    def place(self, display):
        """
        Sets location on display to this x y
        """
        for i in range(0, self.width):
            display.change(self.y, self.x + i, self.string[i])


class TestRightMover(VisibleObject):
    """
    A test object
    """
    def __init__(self):
        VisibleObject.__init__(self, -1, 0, 1, '&')

    def update(self, state):
        state.display.change(self.y, self.x, '.')
        self.right(1)
        self.place(state.display)


class TextScroll(VisibleObject):
    """
    Text that scrolls across screen, right to left
    """
    def __init__(self, text):
        width = len(text)
        x = 28
        y = 0
        VisibleObject.__init__(self, x, y, width, text)

    def update(self, state):
        self.place(state.display)
        self.left()
        if self.x + self.width < 0:
            try:
                i = state.game_objects.index(self)
                state.game_objects.pop(i)
            except ValueError:
                print("tried to remove a game element not in list!")


class Spinner(VisibleObject):
    """
    An object that cycles through different characters
    :param x: The x coordinate
    :type x: int
    :param y: The y coordinate
    :type y: int
    :param chars: the characters to cycle through
    :type chars: List<char>
    :param count: how many updates before next char, default 1
    :type count: int
    """
    def __init__(self, x, y, chars, count=1):
        VisibleObject.__init__(self, x, y, 1, chars[0])
        self.count = count
        self.chars = chars
        self.index = 0
        self.counter = 0

    def update(self, state):
        self.place(state.display)
        self.counter += 1
        if self.counter == self.count:
            self.counter = 0
            self.index += 1
        if self.index >= len(self.chars):
            self.index = 0
        self.string = self.chars[self.index]


