"""
Display is two 16 character lines, held in a 2D array

Display holds the character values at each index
"""
import os  # for clearing console on console printer
import sys   # for clearing console on console printer


class Display:
    """
    Holds values to display and prints them

    Calls self.printer(rows) to print 2 16 char rows of text with its printer property

    Starts with space character in each location.

    Starts with a ConsolePrinter as its printer; replace with HitachiDisplay after initialization to use Hitachi
    """
    def __init__(self):
        self.rows = []
        for row_num in range(0, 2):
            row = []
            for col in range(0, 16):
                row.append(' ')
            self.rows.append(row)
        self.printer = ConsolePrinter()
        self.changed = False

    def blank(self):
        """
        Sets all rows and columns to space character
        """
        for r in self.rows:
            for c in range(0, len(r)):
                r[c] = ' '

    def print(self):
        """
        Calls self.printer.print(self.rows)

        Printer is set by default to a Console Printer but this can be changed to, for example a printer for a Hitachi HD444780
        """
        if self.changed:
            self.printer.print(self.rows)
        self.changed = False

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
            if self.rows[row][column] != new:
                self.rows[row][column] = new
                self.changed = True


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
        if sys.platform == 'win32':
            os.system('cls')
        # else:
        #    os.system('clear')
        print(row_string)
