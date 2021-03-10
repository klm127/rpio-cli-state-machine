"""
For displaying text on a Hitachi HD44780U

SCL should be to PI's SCL
SDA should be to PI's SDA

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

class HD44780U_Interface:
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
        time.sleep(DELAY)

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
            
        
