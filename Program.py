import States


class Program:
    def __init__(self):
        self.state = States.InitialState(self)
        self.name = "~ State Machine Program ~"

    def execute(self, inp):
        print('executing ' +inp)
        self.state.execute(inp)

    def get_input(self):
        self.state.print_status()
        t = input('~~> ')
        if t == "exit":
            print('  Goodbye!  ')
            exit(69)
        else:
            self.execute(t)


