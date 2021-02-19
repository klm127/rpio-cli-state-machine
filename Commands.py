class Command: # commands are given a test. If bool_func evaluates to true, they call effect
    def __init__(self, state, bool_func, effect, name='untitled'):
        self.state = state # commands their wrapping state which they pass to effect and they bool_func
        self.bool_func = bool_func
        self.effect = effect
        self.name = name

    def check_command(self, test):
        if self.bool_func(self.state, test) is True:
            self.effect(self.state, test)
            return True
        else:
            return False


class Commands:
    def __init__(self, state): # state is currently unused here
        self.commands = []

    def check_commands(self,test): # tells each command to check itself agsint the value and returns true on the first success it finds
        for c in self.commands:
            if c.check_command(test):
                return True
        return False

    def add(self, command):
        self.commands.append(command)

    def to_string(self): # for "help" cli command - prints bindings
        s = ''
        for c in self.commands:
            s += c.name + ' = ' + str(c.bool_func) + '    calls     ' + str(c.effect) + '\n'
        return s
