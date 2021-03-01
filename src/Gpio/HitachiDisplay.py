"""
Can be passed in as printer object to a Game.Display instance

This class enables an Hitachi HD44780U to be used to run the pirate game. (Or anything else Display is used for)

Currently running in 4 bit. Soon to be changed to 8-bit.

Works with I2C protocol.

To set up, Wire SCL on a Hitachi hat to SCL on the PI. SDA to SDA. Ground to ground and power to 5v.
"""

import time
import smbus


LINE_1 =       0b10000000
LINE_2 =       0b11000000

BACKLIGHT =        0b1000

ENABLE =            0b100

CMD_4BIT =       0b101000
CMD_CLEAR =           0b1
CMD_HOME =           0b10
CMD_POSITION = 0b10000000

DELAY = 0.0005

CMD_MODE = 0
DATA_MODE = 1


class HitachiPrinter:
    """
    Wraps functions for interfacing with a Hitachi HD44780 display. Set src.Game.Map.Display.printer to an instance of this object.
    :param address: The i2C address of the display
    :type address: int
    :param width: the max characters displayed per line
    :type width: int
    """
    def __init__(self, address = 0b100111, width = 16):
        self.ADDRESS = address
        self.LCD_WIDTH = width
        self.bus = smbus.SMBus(1)
        self.lcd_init()

    def lcd_init(self):
        """
        Initializes the LCD with some prior commands
        """
        self.lcd_byte(0b110011, CMD_MODE)
        self.lcd_byte(0b110010, CMD_MODE)
        self.lcd_byte(0b000110, CMD_MODE)
        self.lcd_byte(0b001100, CMD_MODE)
        self.lcd_byte(0b101000, CMD_MODE)
        self.lcd_byte(0b000001, CMD_MODE)
        self.custom_char()
        time.sleep(DELAY)

    def custom_char(self):
        """
        Loads three custom characters into the Hitachi CGRAM for char(0), char(1), and char(2).
        char(0) is a stick figure player object
        char(1) is a left half of a pirate face
        char(2) is the right half of a pirate face
        """
        self.lcd_byte(0b1000000, CMD_MODE)  # set to CGRAM
        # write each byte of the character. 1s are where it will be dark.
        # player char
        self.lcd_byte(0b01110, DATA_MODE)
        self.lcd_byte(0b00100, DATA_MODE)
        self.lcd_byte(0b11111, DATA_MODE)
        self.lcd_byte(0b10101, DATA_MODE)
        self.lcd_byte(0b10101, DATA_MODE)
        self.lcd_byte(0b00100, DATA_MODE)
        self.lcd_byte(0b01110, DATA_MODE)
        self.lcd_byte(0b11011, DATA_MODE)
        # pirate left
        self.lcd_byte(0b01111, DATA_MODE)
        self.lcd_byte(0b10000, DATA_MODE)
        self.lcd_byte(0b10011, DATA_MODE)
        self.lcd_byte(0b10001, DATA_MODE)
        self.lcd_byte(0b11000, DATA_MODE)
        self.lcd_byte(0b11111, DATA_MODE)
        self.lcd_byte(0b01100, DATA_MODE)
        self.lcd_byte(0b01111, DATA_MODE)
        # pirate right
        self.lcd_byte(0b11110, DATA_MODE)
        self.lcd_byte(0b11001, DATA_MODE)
        self.lcd_byte(0b01101, DATA_MODE)
        self.lcd_byte(0b01111, DATA_MODE)
        self.lcd_byte(0b00011, DATA_MODE)
        self.lcd_byte(0b11111, DATA_MODE)
        self.lcd_byte(0b01110, DATA_MODE)
        self.lcd_byte(0b11110, DATA_MODE)

    def lcd_toggle_enable(self, bits):
        """
        Writes to 4 bits to i2c address

        Not called directly; called by lcd_byte.

        :param bits: 4 bits to send
        :type bits: binary
        """
        time.sleep(DELAY)
        self.bus.write_byte(self.ADDRESS, (bits | ENABLE ))
        time.sleep(DELAY)
        self.bus.write_byte(self.ADDRESS, (bits & ~ENABLE ))
        time.sleep(DELAY)

    def lcd_byte(self, bits, mode):
        """
        Splits 8 bits into 4 bit sections.

        Sends the "high" bit to lcd_toggle_enable first, then the "low" bits.

        Sets mode to mode, 0 for a command, 1 to write data to the Hitachi register

        :param bits: 8 bits to write
        :type bits: int
        :param mode: data or command mode
        :type mode: bit
        """
        bits_high = mode | (bits & 0xF0) | BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | BACKLIGHT
        
        self.bus.write_byte(self.ADDRESS, bits_high)
        self.lcd_toggle_enable(bits_high)
        
        self.bus.write_byte(self.ADDRESS, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_string(self, message, line):
        """
        Splits a string into component characters and sends them to hitachi, writing them on the given line
        Note that only lines 1 and 2 are visible on most displays, and that's all this game program supports for now.

        Should not be called externally; use print() instead.

        :param message: A string to write on the display
        :type message: str
        :param line: The line to write to; use constant LINE_1 or LINE_2.
        :type line: int
        """
        message = message.ljust(self.LCD_WIDTH," ")
        self.lcd_byte(line, CMD_MODE)
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]),DATA_MODE)

    def print(self, rows):
        """
        Called by Display to print the current game characters on the display.

        Prints the first array in rows to the top line and the second to the bottom line.

        :param rows: A 2D array of 16 characters each
        :type rows: array
        """
        self.lcd_string(''.join(rows[0]), LINE_1)
        self.lcd_string(''.join(rows[1]), LINE_2)
            
        
