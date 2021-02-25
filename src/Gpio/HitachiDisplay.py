"""
Can be passed in as printer object to a Game.Display instance
For a Hitachi HD44780U to be used to run pirate game


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
    def __init__(self, address = 0b100111, width = 16):
        self.ADDRESS = address
        self.LCD_WIDTH = width
        self.bus = smbus.SMBus(1)
        self.lcd_init()

    def lcd_init(self):
        self.lcd_byte(0b110011, CMD_MODE)
        self.lcd_byte(0b110010, CMD_MODE)
        self.lcd_byte(0b000110, CMD_MODE)
        self.lcd_byte(0b001100, CMD_MODE)
        self.lcd_byte(0b101000, CMD_MODE)
        self.lcd_byte(0b000001, CMD_MODE)
        self.custom_char()
        time.sleep(DELAY)

    def custom_char(self):
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
        time.sleep(DELAY)
        self.bus.write_byte(self.ADDRESS, (bits | ENABLE ))
        time.sleep(DELAY)
        self.bus.write_byte(self.ADDRESS, (bits & ~ENABLE ))
        time.sleep(DELAY)

    def lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | BACKLIGHT
        
        self.bus.write_byte(self.ADDRESS, bits_high)
        self.lcd_toggle_enable(bits_high)
        
        self.bus.write_byte(self.ADDRESS, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_string(self, message, line):
        message = message.ljust(self.LCD_WIDTH," ")
        self.lcd_byte(line, CMD_MODE)
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]),DATA_MODE)

    def print(self, rows):
        self.lcd_string(''.join(rows[0]), LINE_1)
        self.lcd_string(''.join(rows[1]), LINE_2)
            
        
