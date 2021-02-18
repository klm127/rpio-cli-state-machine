class Command:
    def __init__(self, state, bool_func, effect, name='untitled'):
        self.state = state
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
    def __init__(self, state):
        self.commands = []

    def check_commands(self,test):
        for c in self.commands:
            if c.check_command(test):
                return True
        return False

    def add(self, command):
        self.commands.append(command)

    def to_string(self):
        s = ''
        for c in self.commands:
            s += f'{c.name} = {c.bool_func}   calls   {c.effect}\n'
        return s
