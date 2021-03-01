"""
Generates `Maps` from text data.
"""

from src.Game.Map import Map, MapObject, Player, Tile


class Level:
    """
    Generates a map from a string array, following these rules:
    The map will be as wide as the first row in the string array.
    The @ symbol indicates player start location, otherwise it will be 0,0.
    A '.', '=', ':', or ' ' will generate a (passable) floor object.
    A '$' will generate a `WinZone` object at that location which, when reached, allows level ascension.
    An 'l' will generate an animated lava tile that, when touched, results in a Game Over.

    :param str_arr: An array of strings representing level design.
    :type str_arr: Array<string>
    """
    def __init__(self, str_arr):
        self.str_arr = str_arr
        self.player_x = 0
        self.player_y = 0
        self.win_x = -1
        self.win_y = -1
        self.height = len(str_arr)
        self.width = len(str_arr[0])
        self.map_arr = []
        for y in range(0, self.height):
            row = []
            for x in range(0, self.width):
                if y > len(str_arr) - 1 or x > len(str_arr[y]):
                    row.append(Map.MapSquare(x, y, Tile.Wall, 'X' ))
                else:
                    c = str_arr[y][x]
                    if c == '.' or c == '=' or c == ':' or c == ' ':  # floor
                        row.append(Map.MapSquare(x, y, Tile.Floor, c))
                    elif c == '@': # player
                        self.player_x = x
                        self.player_y = y
                        row.append(Map.MapSquare(x, y, Tile.Floor, ':'))
                    elif c == '$': # win
                        self.win_x = x
                        self.win_y = y
                        sq = Map.MapSquare(x, y, Tile.Floor, ':')
                        win = MapObject.WinZone(True)
                        sq.objects.append(win)
                        row.append(sq)
                    elif c == 'l':  # lava
                        sq = Map.MapSquare(x, y, Tile.Floor, '.')
                        lav = MapObject.Lava(True)
                        sq.objects.append(lav)
                        row.append(sq)
                    else:
                        row.append(Map.MapSquare(x, y, Tile.Wall, c))
            self.map_arr.append(row)

    def get_map(self):
        return Map.Map(self.map_arr, self.player_x, self.player_y)


class Levels:
    """
    Levels.levs contains Levels generated from string arrays. `MapState` holds an index of the current level and
    retrieves it from `Levels.levs`.
    """
    levs = [
    Level([
        ". |`|.|XXXXXX..           $ ",
        "...@  =======. .Fundamentals",
        ".     |XXXXX|Systems````````",
        ".. .. 430```````````        ",
        "..COMP.|....................",
        "..|........................."
    ]),
    Level([
        "..  .llllllllllllllllllllllllllll. .",
        "..  .======llllllllllllll========. .",
        " @LAVAllll=====llllll=====lllllll. .",
        "CAREFULlllllll========lllllllllll $ "
    ]),
    Level([
        "....|0|..../\/\/\............XXX.. .... ().0ll&++++++++",
        "..=.....     ...|.=|l______..XXX.XXXXX .() Oll&++++++++",
        "..... .......... ... ______..---=----X. ().=..&-Pirate-",
        ". .COMP-430...         ....| .....  .|.... O..  .   . $ "
        ])
    ]
