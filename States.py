from Commands import *
from GpioUtil import *
import RPi.GPIO as GPIO


class State:

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
        state.program.get_input()

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


class InitialState(State): # just adds two more commands - gpio-001 and cli-mode

    def __init__(self, program):
        State.__init__(self, program)
        self.commands.add(Command(self, State.get_check_string_cb("cli-mode"), State.send_text_state, 'cli-mode'))
        self.commands.add(Command(self, State.get_check_string_cb("gpio-001"), State.send_gpio_1,'gpio-001'))

class TextInputState(InitialState):

    def __init__(self, program):
        InitialState.__init__(self, program)
        self.commands.add(Command(self, State.get_check_string_cb("gpio-mode"), State.send_gpio_state, 'gpio-mode'))
        program.name = '~ State Machine : Text Input State ~'

    def end_state(self):
        super().end_state()

    def execute(self, inp): # besides executing command, calls get_input() in program to keep it looping for more commands
        b = self.commands.check_commands(inp)
        if not b:
            print(' x Command Not Recognized x ')
        self.program.get_input()


class GpioState(TextInputState):
    def __init__(self, program):
        TextInputState.__init__(self, program)
        program.name = '~ State Machine : GPIO Input State ~'
        # gpiostate has two separate command sections... one for dealing with string calls and one for dealing with button press events sent from LongSwitch
        self.gpio_commands = Commands(self)
        self.commands.add(Command(self, State.get_front_check_string_cb('sim'), GpioState.sim_command))
        self.pins = {}
        # maps pins to associated LongSwitch instance

    def long_press_cb(self, pin, press_time, rise=GPIO.RISING, target_press_time=1000, end_after=50):
        # generates a callback for checking a press event
        # also initializes LongPress for that pin if it hasn't been yet
        # if it has been initialized and properties of it have been changed, it changes those properties
        if pin in self.pins:
            pin.press_time = press_time
            pin.rise = rise
            pin.end_after = end_after
        else:
            self.pins[pin] = LongSwitch(self, pin, rise, end_after)

        def cb(state, test):
            if test["length"] >= target_press_time:
                return True
            else:
                return False
        return cb

    def execute(self, inp):
        if type(inp) == str: # if a string, it handles via TextInputState and checks against regular Commands
            super().execute(inp)
        else: # if not a string, it handles in a special way
            self.execute_gpio(inp)

    def execute_string(self, inp):
        b = self.commands.check_commands(inp)
        return b

    def execute_gpio(self, inp):
        print('input: ' + str(inp))
        b = self.gpio_commands.check_commands(inp)
        return b

    #todo: new help function that includes gpio commands

    @staticmethod
    def sim_command(state, value): # turns a cli command like "sim 1 1000" into an input object representing that button press
        gpio_sim = get_sim_gpio(value) # from GpioUtil
        state.execute(gpio_sim)

    @staticmethod
    def print_switch_info(state, inp):
        print('in state: ' + str(state))
        print('input detected:')
        print(str(inp))


class GpioState1(GpioState):
    def __init__(self, program):
        GpioState.__init__(self, program)
        GPIO.setmode(GPIO.BCM)
        self.gpio_commands.add(Command(self, self.long_press_cb(21,1000), GpioState.print_switch_info))



