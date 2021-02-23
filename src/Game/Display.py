"""
Display is two 28 character lines

Display holds the character values at each index
"""


class Display:
    """
    Holds values to display and prints them

    Calls self.printer(rows) to print 2 28 char rows of text with its printer property
    """
    def __init__(self):
        self.rows = []
        for row_num in range(0, 2):
            row = []
            for col in range(0, 28):
                row.append('.')
            self.rows.append(row)
        self.printer = ConsolePrinter()

    def blank(self):
        for r in self.rows:
            for c in range(0, len(r)):
                r[c] = '.'

    def print(self):
        """
        Calls self.printer.print(self.rows)

        Printer is set by default to a Console Printer but this can be changed to, for example a printer for a Hitachi HD444780
        """
        self.printer.print(self.rows)

    def change(self, row, column, new):
        """
        Changes the character at a position in the display

        :param row: The row to target
        :type row: int
        :param column: The column to target
        :type column: int
        :param new: the new character to replace with
        :type new: char
        """
        if len(self.rows) > row >= 0 and len(self.rows[0]) > column >= 0:
            self.rows[row][column] = new


class ConsolePrinter:
    """
    utility class for printing to console
    """
    def print(self, rows):
        """
        Prints two 28 character rows to console

        :param rows: a 2D array, containing 2 sub-arrays, each with 28 chars
        """
        row_string = '\n'
        for row in rows:
            for val in range(0, len(row)):
                row_string += row[val]
            row_string += '\n'
        print(row_string)
