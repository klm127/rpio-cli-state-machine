"""
Runs the program

Program entry point. Initializes an instance of the Program class, then sends
an execute command program.

'program.execute('gpio-10-press 21 19')

This will put the program in the gpio 10 press state with GPIO pin 21
set to an input switch and GPIO pin 19 set to an output LED.

"""

from Program import Program

program = Program()

program.execute('gpio-10-press 21 19')
