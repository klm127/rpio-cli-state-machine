from src.Game.Map import Map, MapObject, Player, Tile


class Level:
    def __init__(self, str_arr):
        self.str_arr = str_arr
        self.player_x = 0
        self.player_y = 0
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
                    if c == '.' or c == '=' or c == ':' or c == ' ':
                        row.append(Map.MapSquare(x, y, Tile.Floor, c))
                    elif c == '@':
                        self.player_x = x
                        self.player_y = y
                        row.append(Map.MapSquare(x, y, Tile.Floor, ':'))
                    else:
                        row.append(Map.MapSquare(x, y, Tile.Wall, c))
            self.map_arr.append(row)

    def get_map(self):
        return Map.Map(self.map_arr, self.player_x, self.player_y)


class Levels:
    demo = Level([
        "..|`|.|XXXXXX...............",
        "...@..=======...Fundamentals",
        "......|XXXXX|Systems........",
        "......430...................",
        "..COMP......................",
        "............................"
    ])
