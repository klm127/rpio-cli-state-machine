from Commands import *
from GpioUtil import *
import RPi.GPIO as GPIO


class State:
    """
    Parent class for states to extend
    
    Initializes a `Commands` object and creates a `Command` which binds input text "help" to an 
    effect that prints the commands available in the current state.

    Also defines static methods for serving various states.
        
    :param program: The running instance of `Program`
    :type program: class Program

    """

    def __init__(self, program):
        self.program = program
        self.commands = Commands(self)
        self.commands.add(Command(self, State.get_check_string_cb("help"), self.print_help, 'help'))

    def execute(self, inp):
        """
        Checks input to see if any Command in `self.commands` matches input.
        
        :param inp: Input sent by `Program.execute`.
        :type inp: str | Dict
        :returns: Whether a matching command was found for the input.
        :rtype: boolean
        
        """
        b = self.commands.check_commands(inp)
        return b

    def end_state(self):
        """
        Lifecycle method called when a new state is loaded. Clears Commands.
        
        """
        self.commands.commands = []

    def print_status(self):
        """
        Prints program.name to console between inputs. Can be overwritten by extending classes to print something else.
        
        """
        print(self.program.name)

    @staticmethod
    def print_help(state, inp):
        """
        Prints information about commands this state can perform to the console.
        
        A callback method that should be passed to a `Command` object on initialization as the `effect` parameter.
        
        :param state: The state in which the `Command` exists
        :type state: class State
        :param inp: The input the `Command` parsed
        :type inp: str
        
        """
        print(state.commands.to_string())

    @staticmethod
    def send_initial_state(state, test=''):
        """
        Loads an instance of `InitialState` into the program state and ends the previous state.
        
        A callback method that should be passed to a `Command` object on initialization as the `effect` parameter.
        
        :param state: The state in which the `Command` exists
        :type state: class State
        :param inp: The input the `Command` parsed
        :type inp: str
        
        """
        state.program.state = InitialState(state.program)
        state.end_state()

    @staticmethod
    def send_text_state(state, test=''): 
        """
        Loads an instance of `TextInputState` into the program state and ends the previous state.
        
        A callback method that should be passed to a `Command` object on initialization as the `effect` parameter.
        
        :param state: The state in which the `Command` exists
        :type state: class State
        :param inp: The input the `Command` parsed
        :type inp: str
        
        """
        state.program.state = TextInputState(state.program)
        state.end_state()
        state.program.get_input()

    @staticmethod
    def send_gpio_state(state, test=''):
        """
        Loads an instance of `GpioState` into the program and ends the previous state.
        
        A callback method that should be passed to a `Command` object on initialization as the `effect` parameter.
        
        :param state: The state in which the `Command` exists
        :type state: class State
        :param inp: The input the `Command` parsed
        :type inp: str
        
        """
        state.program.state = GpioState(state.program)
        state.end_state()
        state.program.wait()

    @staticmethod
    def send_gpio_10_press(state, test=''):
        """
        Loads an instance of the `Gpio_10_Press` state into the program and ends the previous state.
        
        A callback method that should be passed to a `Command` object on initialization as the `effect` parameter.
        
        This method is meant to be used as an `effect` with a callback from `get_front_check_string_cb` as the `bool_func` in the `Command` object. It expects there to be parameters in the input string; two integers, one for the switch pin and one for the LED pin. If there are not, it loads a new instance of `Gpio_10_Press` with 21 for the switch parameter and 19 for the LED parameter.
        
        :param state: The state in which the `Command` exists
        :type state: class State
        :param inp: The input the `Command` parsed
        :type inp: str
        
        """
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

    @staticmethod
    def get_check_string_cb(target_str):
        """
        A method to generate a callback function that should be passed to a `Command` object
        on initialization as the `bool_func` parameter. The callback will compare an input 
        to `target_str` and, if it matches exactly, returns true. Otherwise, it returns false.
        
        :param target_str: A string to test inputs against
        :type param: str
        :returns: A callback function to pass to a `Command` object.
        :rtype: Function
        """

        def cb(state, test_str):
            if target_str == test_str:
                return True
            else:
                return False
        return cb

    @staticmethod
    def get_front_check_string_cb(target_str): 
        """
        Returns a callback that will test the front part of an input string against a given value, and return true if that portion matches. Enables the inclusion of options/additional parameters with the Program or State `.execute` method. 
        
        Callback to be used with the `bool_func` parameter of a `Command` object.
        
        :param target_str: A string to test the front part of an input string against.
        :type param: str
        :returns: A callback for use with a `Command` object.
        :rtype: Function
        """
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
    to cli-mode (`TextInputState`) and one for changing program state to
    `Gpio_10_press`
    """

    def __init__(self, program):
        State.__init__(self, program)
        self.commands.add(Command(self, State.get_check_string_cb("cli-mode"), State.send_text_state, 'cli-mode'))
        self.commands.add(Command(self, State.get_front_check_string_cb("gpio-10-press"), State.send_gpio_10_press,'gpio-10-press'))

class TextInputState(InitialState):
    """
    A CLI type state

    Creates a gpio-mode command and changes program.name
    
    :param program: The running `Program` instance.
    :type param: class Program
    
    """
    def __init__(self, program):
        InitialState.__init__(self, program)
        self.commands.add(Command(self, State.get_check_string_cb("gpio-mode"), State.send_gpio_state, 'gpio-mode'))
        program.name = '~ State Machine : Text Input State ~'

    def execute(self, inp):
        """
        Checks input against commands. Prints an error if the command is not recognized. Afterwards, calls `self.program.get_input()` to get more input.
        
        :param inp: Input to check against `self.commands`
        :type inp: str
        """
        b = self.commands.check_commands(inp)
        if not b:
            print(' x Command Not Recognized x ')
        self.program.get_input()


class GpioState(InitialState):
    """
    A state for handling GPIO input events

    Changes program state to a mode which handles GPIO events. Clears out inherited commands and creates a new `Commands` object for use with GPIO-based commands.
    
    Contains a dictionary, `self.pins`, with keys corresponding to pins and values corresponding to objects from `GpioUtil`.
        
    :param program: A `Program` instance.
    :type program: class Program
    
    """
    def __init__(self, program):
        InitialState.__init__(self, program)
        program.name = '~ State Machine : GPIO Input State ~'
        self.commands = Commands(self)
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
        self.light_times = [] # holds 10 floats repr. switch-press lengths 
        self.flasher = Led(led)
        self.commands.add(Command(self, self.press_cb(switch), GpioState_10_press.light_time_append))

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
        print('appending light time #'+str(len(state.light_times))+" : " + str(inp["length"]))
        if len(state.light_times) < 10:
            state.light_times.append(inp["length"])
        else:
            state.flash_light(inp)

    def flash_light(self,inp):
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

    



