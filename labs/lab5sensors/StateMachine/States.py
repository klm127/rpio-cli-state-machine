from StateMachine.Commands import *


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
        self.commands.add(Command(self, State.get_check_string_cb("help"), self.print_help, 'help'))
        self.commands.add(Command(self, State.get_check_string_cb("cli-mode"), State.send_text_state, 'cli-mode'))


class TextInputState(InitialState):
    """
    A CLI type state

    Creates a Gpio-mode command and changes program.name
    
    :param program: The running `Program` instance.
    :type param: class Program
    
    """
    def __init__(self, program):
        InitialState.__init__(self, program)
        self.commands.add(Command(self, State.get_check_string_cb("Gpio-mode"), State.send_gpio_state, 'Gpio-mode'))
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




    



