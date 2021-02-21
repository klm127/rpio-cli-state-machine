"""
Class for managing the active state.
"""

import States
import time


class Program:
    """
    Holds current state and sends execution to that state.
    
    On initialization, sets `self.state` to an instance of `States.InitialState(self)`
    
    """

    def __init__(self):
        self.state = States.InitialState(self)
        self.name = "~ State Machine Program ~"

    def execute(self, inp):
        """
        Sends an input event to a state for execution and prints that event. Called by states to ensure executions are always sent to the active state.
        
        :param inp: Input, possibly from CLI, possibly from another source
        :type inp: str | dict
       
        """
        print('executing ' +inp)
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
