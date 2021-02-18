from Commands import *
from GpioUtil import *


class State:

    def __init__(self, program):
        self.program = program
        self.commands = Commands(self)
        self.commands.add(Command(self, State.get_check_string_cb("help"), self.print_help, 'help'))

    def execute(self, inp):
        b = self.commands.check_commands(inp)
        return b

    def end_state(self):
        self.commands.commands = []

    def print_help(self, state, inp):
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
    def get_front_check_string_cb(target_str, length):

        def cb(state, test_str):
            chunk = test_str[0:length]
            if chunk == target_str:
                return True
            else:
                return False
        return cb


class InitialState(State):

    def __init__(self, program):
        State.__init__(self, program)
        self.commands.add(Command(self, State.get_check_string_cb("cli-mode"), State.send_text_state, 'cli-mode'))


class TextInputState(InitialState):

    def __init__(self, program):
        InitialState.__init__(self, program)
        self.commands.add(Command(self, State.get_check_string_cb("gpio-mode"), State.send_gpio_state, 'gpio-mode'))
        program.name = '~ State Machine : Text Input State ~'

    def end_state(self):
        super().end_state()

    def execute(self, inp):
        b = self.commands.check_commands(inp)
        if not b:
            print(' x Command Not Recognized x ')
        self.program.get_input()


class GpioState(TextInputState):
    def __init__(self, program):
        TextInputState.__init__(self, program)
        program.name = '~ State Machine : GPIO Input State ~'
        self.gpio_commands = Commands(self)
        self.pins = {}

    def long_press_cb(self, pin, press_time, rise, target_press_time=1000, end_after=50):
        if pin in self.pins:
            pin.press_time = press_time
            pin.rise = rise
            pin.end_after = end_after
        else:
            self.pins[pin] = LongSwitch(self, pin, rise, end_after)

        def cb(state, test):
            if test.length >= target_press_time:
                return True
            else:
                return False
        return cb

    def execute(self, inp):
        if type(inp) == str:
            super().execute(inp)
        else:
            self.execute_gpio(inp)

    def execute_string(self, inp):
        b = self.commands.check_commands(inp)
        return b

    def execute_gpio(self, inp):
        b = self.gpio_commands.check_commands(inp)
        return b

    @staticmethod
    def sim_command(state, value):
        gpio_sim = get_sim_gpio(value)
        state.execute(gpio_sim)

    def print_switch_info(self, state, inp):
        print(self)
        print('input detected:')
        print(inp)






