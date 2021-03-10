"""
Classes for binding conditions to effects on the state of the program, using callback functions for input testing and state effect alteration. 
"""


class Command:
    """
    Binds an evaluation callback to an effect callback.

    :param state: The state using this Command
    :type state: class State
    :param bool_func: A callback which returns True if the effect should be triggered
    :type bool_func: Function
    :param effect: A callback called when command should be executed
    :type effect: Function
    :param name: Optional parameter containing human-readable command name
    :type name: str

    """
    def __init__(self, state, bool_func, effect, name='untitled'):
        self.state = state
        self.bool_func = bool_func
        self.effect = effect
        self.name = name

    def check_command(self, test):
        """
        Checks test with `self.bool_func(self.state, test)` callback. If true, calls `self.effect(self.state, test)`
        
        :param test: Input to test.
        :type test: str | dict
        
        """    
        if self.bool_func(self.state, test) is True:
            self.effect(self.state, test)
            return True
        else:
            return False


class Commands:
    """
    Contains a list of Command objects
    
    :param state: The state containing this Commands object 
    :type state: class State
    
    """
    def __init__(self, state):
        self.commands = []

    def check_commands(self,test):
        """
        Checks each command and returns True on the first match it has. Otherwise, returns False.
        
        :param test: An input to test against each command.
        :type test: str | dict
        
        """
        for c in self.commands:
            if c.check_command(test):
                return True
        return False

    def add(self, command):
        """
        Adds a `Command` to `self.commands`
        
        :param command: A `Command` to append to `self.commands`
        :type command: class Command
        
        """
        self.commands.append(command)

    def to_string(self): # for "help" cli command - prints bindings
        """
        Provides a string listing `Command` bindings and their names, separated by newlines.
        
        :returns: Information about available commands.
        :rtype str:

        """
        s = ''
        for c in self.commands:
            s += c.name + ' = ' + str(c.bool_func) + '    calls     ' + str(c.effect) + '\n'
        return s
