"""
Class for managing the active state.
"""

from src.StateMachine import States


class Program:
    """
    Holds current state and sends execution to that state.
    
    On initialization, sets `self.state` to an instance of `States.InitialState(self)`

    :param state: The Initial State
    :type state: class State
    
    """

    def __init__(self):
        self.state = States.InitialState(self)
        self.name = "~ State Machine Program ~"
        self.verbose = True

    def load_state(self, new_state):
        """
        Ends the old state and loads new state

        :param new_state: A new state to load
        :type new_state: class State
        """
        print('load state called')
        self.state.end_state()
        print('closed state ' + str(self.state))
        self.state = new_state
        print('new state ' + str(self.state))

    def execute(self, inp):
        """
        Sends an input event to a state for execution and prints that event. Called by states to ensure executions are always sent to the active state.
        
        :param inp: Input, possibly from CLI, possibly from another source
        :type inp: str | dict
       
        """
        if self.verbose:
            print('executing ' + str(inp))
        self.state.execute(inp)

    def get_input(self):
        """
        Gets text input for use with cli-type states. Calls `print_status()` on the current state which usually just prints `ProgramInstance.name`. Checks if text input is "exit" and, if it is, exits the program. Otherwise, sends input to the active state to execute.
        """
        self.state.print_status()
        t = input('~~> ')
        if t == "exit":
            print('  Goodbye!  ')
            exit(69)
        else:
            self.execute(t)
