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
    def send_text_state(state, test=''): # sends new state to program - this would be mapped to "effect" callback of a command. I.e. "cli-mode" changes the state to text-input
        state.program.state = TextInputState(state.program)
        state.end_state()
        state.program.get_input()

    @staticmethod
    def send_gpio_state(state, test=''):
        state.program.state = GpioState(state.program)
        state.end_state()
        state.program.wait()

    @staticmethod
    def send_gpio_1(state, test=''):
        state.program.state = GpioState1(state.program)
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
    def get_front_check_string_cb(target_str): # creates a callback for use with Command that checks to see if a tested input string matches at the beginning (but not necessarily all the way)
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
    GpioState1
    """

    def __init__(self, program):
        State.__init__(self, program)
        self.commands.add(Command(self, State.get_check_string_cb("cli-mode"), State.send_text_state, 'cli-mode'))
        self.commands.add(Command(self, State.get_check_string_cb("gpio-001"), State.send_gpio_1,'gpio-001'))

class TextInputState(InitialState):
    """
    A CLI type state

    Creates a gpio-mode command and changes program.name

    Methods
    -------
    self.execute(self, inp) : overwrites State.execute. As parent,
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
        prints an error. Otherwise, calls execute_gpio
    self.execute_gpio(self, input) -> bool: Checks input against commands 
        and returns true if input matches any command

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
        if type(inp) == str:
            print('String input invalid in GPIO state')
        else: 
            self.execute_gpio(inp)

    def execute_gpio(self, inp):
        print('input: ' + str(inp))
        b = self.commands.check_commands(inp)
        return b

    @staticmethod
    def print_switch_info(state, inp):
        print('in state: ' + str(state))
        print('input detected:')
        print(str(inp))


class GpioState1(GpioState):
    def __init__(self, program):
        GpioState.__init__(self, program)
        GPIO.setmode(GPIO.BCM)
        self.commands.add(Command(self, self.press_cb(21), GpioState.print_switch_info))



