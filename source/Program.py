import States


class Program:
    """
    Holds current state and sends execution to that state

    Attributes
    ----------
    self.state : State The active state
    self.name : str Program name, sometimes changed by states

    Methods
    -------
    execute(self, inp) : sends input to to active state. Input may be string or other object depending on state
    get_input(self) : gets text input for cli states

    """

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


