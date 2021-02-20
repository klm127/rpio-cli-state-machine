from Commands import *
from GpioUtil import *
import RPi.GPIO as GPIO


class State:
    """
    Parent class for states to extend

    Attributes
    ----------
    self.program : Program The Program class where this state is running
    self.commands : Commands A command object containing available commands in this state

    Methods
    -------
    self.execute(self, inp) -> bool : Checks commands to see if input triggers any of them
    self.end_state(self, inp) : Ends the state by clearing commands
    self.print_help(self, state, inp) : Called by a command - prints command bindings
    self.print_status(self) : Prints current program name

    Static Methods
    --------------
    Passed as callbacks in effect parameter on Command creation

    State.send_initial_state(state, test='') : Sets program instance's active state to an InitialState instance
    State.send_text_state(state, test='') : Sets program state to Text input state
    State.send_gpio_state(state, test='') : Sets program state to base GPIO state
    State.send_gpio_1(state, test='') : Sets program state to GPIO 1 state
    State.get_check_str_cb(target_str : str) - > Function :
        Returns a callback that will evaluate a test string against a target string
    State.get_front_check_str_cb(target_str : str) -> Function :
        Returns a callback that will evaluate the front of a string against a target string

    """

    def __init__(self, program):
        self.program = program
        self.commands = Commands(self)
        self.commands.add(Command(self, State.get_check_string_cb("help"), self.print_help, 'help'))

    def execute(self, inp): # called by Program, whenever it has input to send. Program only calls the active state
        b = self.commands.check_commands(inp)
        return b

    def end_state(self):
        self.commands.commands = []

    def print_help(self, state, inp): # cli - 'help' - prints list of command callback mappings; this is the "effect" callback of Command
        print(self.commands.to_string())

    @staticmethod
    def send_initial_state(state, test=''):
        state.program.state = InitialState(state.program)
        state.end_state()

    @staticmethod
    def send_text_state(state, test=''): 
        state.program.state = TextInputState(state.program)
        state.end_state()
        state.program.get_input()

    @staticmethod
    def send_gpio_state(state, test=''):
        state.program.state = GpioState(state.program)
        state.end_state()
        state.program.wait()

    @staticmethod
    def send_gpio_10_press(state, test=''):
        switch = 21
        led = 19
        testArr = test.split(' ')
        try:
            switch = int(testArr[1])
            led = int(testArr[2])
        except:
            pass
        state.program.state = GpioState_10_press(state.program, switch, led)
        state.end_state()
        state.program.get_input()

    def print_status(self):
        print(self.program.name)

    @staticmethod
    def get_check_string_cb(target_str):

        def cb(state, test_str):
            if target_str == test_str:
                return True
            else:
                return False
        return cb

    @staticmethod
    def get_front_check_string_cb(target_str): 
        def cb(state, test_str):
            chunk = test_str[0:len(target_str)]
            if chunk == target_str:
                return True
            else:
                return False
        return cb


class InitialState(State):
    """
    The initial program state

    Same as state, but adds two commands, one for changing Program state
    to cli-mode (TextInputState) and one for changing program state to
    Gpio_10_press
    """

    def __init__(self, program):
        State.__init__(self, program)
        self.commands.add(Command(self, State.get_check_string_cb("cli-mode"), State.send_text_state, 'cli-mode'))
        self.commands.add(Command(self, State.get_front_check_string_cb("gpio-10-press"), State.send_gpio_10_press,'gpio-10-press'))

class TextInputState(InitialState):
    """
    A CLI type state

    Creates a gpio-mode command and changes program.name

    Methods
    -------
    self.execute(self, inp) : overwrites State.execute. As super,
    checks commands, but also prints an error if a command is not
    recognized and calls program.get_input(), causing the cli to loop.
    """
    def __init__(self, program):
        InitialState.__init__(self, program)
        self.commands.add(Command(self, State.get_check_string_cb("gpio-mode"), State.send_gpio_state, 'gpio-mode'))
        program.name = '~ State Machine : Text Input State ~'

    def execute(self, inp): # besides executing command, calls get_input() in program to keep it looping for more commands
        b = self.commands.check_commands(inp)
        if not b:
            print(' x Command Not Recognized x ')
        self.program.get_input()


class GpioState(InitialState):
    """
    A state for handling GPIO input events

    Changes program state to a mode which handles GPIO events

    Attributes
    ----------
    self.commands : Commands Creates a new Commands object for GPIO
    self.pins : Dictionary A dictionary where key corresponds to pin and
        value is the switch type. Only one should be set at any given time.

    Methods
    -------
    self.press_cb(self, pin) -> Function 
        Returns a callback to pass to a new Command object. The 
        callback returns true if the switch pin matches.
    self.execute(self, input) : Checks if input is a string and, if it is,
        prints an error. Otherwise, checks commands

    Static Methods
    ------
    GPIOState.print_switch_info(state, inp) : Used as a callback for a 
        command. Prints info about the input onto the console.
    """
    def __init__(self, program):
        InitialState.__init__(self, program)
        program.name = '~ State Machine : GPIO Input State ~'
        self.commands = Commands(self)
        self.pins = {}

    def press_cb(self, pin, end_after=5):
        self.pins[pin] = Switch(self, pin)

        def cb(state, test):
            if test["pin"] == pin:
                return True
            else:
                return False
        return cb

    def execute(self, inp):
        b = False
        if type(inp) == str:
            print('String input invalid in GPIO state')
        else: 
            b = self.commands.check_commands(inp)
        return b

    @staticmethod
    def print_switch_info(state, inp):
        print('in state: ' + str(state))
        print('input detected:')
        print(str(inp))


class GpioState_10_press(GpioState):
    """
    10 press flash state

    This state sets up a button and an LED. Button press lengths are recorded. When 10
    button presses are logged, the LED flashes 10 times for those lengths, with a 1
    second delay between flashes.
    """
    def __init__(self, program, switch, led):
        GpioState.__init__(self, program)
        self.light_times = []
        self.lighting = False
        self.flasher = Led(led)
        self.commands.add(Command(self, self.press_cb(switch), GpioState_10_press.light_time_append))

    @staticmethod
    def light_time_append(state, inp):
        print('appending light time #'+str(len(state.light_times))+" : " + str(inp["length"]))
        if len(state.light_times) < 10:
            state.light_times.append(inp["length"])
        else:
            state.flash_light(inp)

    def flash_light(self,inp):
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

    



