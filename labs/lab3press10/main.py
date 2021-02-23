"""
Runs the program

Program entry point. Initializes an instance of the Program class, then sends
an execute command program.

'program.execute('Gpio-10-press 21 19')

This will put the program in the Gpio 10 press state with GPIO pin 21
set to an input switch and GPIO pin 19 set to an output LED.

"""

from src.StateMachine.Program import Program
from src.Gpio import GpioStates

program = Program()
program.state = GpioStates.GpioState_10_press(program, 21, 19)
