"""
States specific to interfacing with pins on a Raspberry PI
"""

from src.StateMachine import *
from GpioUtil import *


class GpioState(States.InitialState):
    """
    A state for handling GPIO input events

    Changes program state to a mode which handles GPIO events. Clears out inherited commands and creates a new `Commands` object for use with GPIO-based commands.

    Contains a dictionary, `self.pins`, with keys corresponding to pins and values corresponding to objects from `GpioUtil`.

    :param program: A `Program` instance.
    :type program: class Program

    """

    def __init__(self, program):
        States.InitialState.__init__(self, program)
        program.name = '~ State Machine : GPIO Input State ~'
        self.commands = Commands.Commands(self)
        self.pins = {}

    def press_cb(self, pin):
        """
        Returns a callback for use with a `Command` object. That callback tests if an input object's `["pin"]` property is equal to the parameter pin, and returns true if it matches.

        :param pin: The pin an input should be checked against
        :type pin: int
        :returns: A callback passed to a `Command` object as the `bool_func` parameter.
        :rtype: Function

        """
        self.pins[pin] = Switch(self, pin)

        def cb(state, test):
            if test["pin"] == pin:
                return True
            else:
                return False

        return cb

    def execute(self, inp):
        """
        Overwrites inherited method. If it is passed a string input, prints an error message and returns false. Otherwise, checks commands.

        :param inp: An input object
        :type inp: str | Dict
        :returns: True if a matching command was found and input was not a string, false otherwise.
        :rtype boolean:

        """
        b = False
        if type(inp) == str:
            print('String input invalid in GPIO state')
        else:
            b = self.commands.check_commands(inp)
        return b

    @staticmethod
    def print_switch_info(state, inp):
        """
        Debug method passed as a callback to a `Command` object in the `effect` parameter. Prints information about input received.

        :param state: The calling state, passed by the `Command` object.
        :type state: class State
        :param inp: The input object, passed by the `Command` object.
        :type inp: dict

        """
        print('in state: ' + str(state))
        print('input detected:')
        print(str(inp))


# noinspection PyPep8Naming
class GpioState_10_press(GpioState):
    """
    10 press flash state

    This state sets up a button and an LED. Button press lengths are recorded. When 10
    button presses are logged, the LED flashes 10 times for those lengths, with a 1
    second delay between flashes.

    :param program: The active `Program` object.
    :type program: class Program
    :param switch: The GPIO Pin a Switch is set on.
    :type switch: int
    :param led: The GPIO Pin an LED is set on.
    :type led: int

    """

    def __init__(self, program, switch, led):
        GpioState.__init__(self, program)
        self.light_times = []  # holds 10 floats repr. switch-press lengths
        self.flasher = Led(led)
        self.commands.add(Commands.Command(self, self.press_cb(switch), GpioState_10_press.light_time_append))

    @staticmethod
    def light_time_append(state, inp):
        """
        A callback method to be passed to `Command` as the `effect` parameter.

        Adds the length of a button press to the `light_times` list in the `GpioState_10_press` object. If that list has more than 10 items, it instead calls `state.flash_light`

        :param state: The calling `State` object, passed by the `Command` object.
        :type state: class Gpio_10_press
        :param inp: The input object.
        :type inp: class Object

        """
        print('appending light time #' + str(len(state.light_times)) + " : " + str(inp["length"]))
        if len(state.light_times) < 10:
            state.light_times.append(inp["length"])
        else:
            state.flash_light(inp)

    def flash_light(self, inp):
        """
        Flashes an LED light ten times. Deactivates input switch while running. Waits 1 second between flashes. When finished, the list of times is empty and the program is ready to repeat.

        :param inp: Input passed by the Commands object. The `Switch` is retrieved from this parameter in order to temporarily deactivate it.
        :type inp: class Dict
        """
        print('Flashing!')
        switch = self.pins[inp["pin"]]
        switch.deactivate()
        while len(self.light_times) > 0:
            flash_time = self.light_times.pop(0)
            self.flasher.on()
            time.sleep(flash_time)
            self.flasher.off()
            time.sleep(1)
        switch.activate()
        print('Done Flashing.')