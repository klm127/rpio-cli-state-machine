State Machine
------------
`rpio-cli-state-machine.src.StateMachine` provides classes for managing states in a Python program. Custom states are created by extending `States.TextInputState`, for cli based programs, or `Gpio.GpioStates.GpioState`, for programs utilizing the RPIO pins of a Raspberry Pi.

Each `State` creates `Commands` on initialization, and adds `Command` objects to it. A `Command` consists of two callbacks; a function to test whether a condition is true and a function to execute if it is true. When `State.execute(input)` is called, it checks its Commands for any Commands whose condition matches the input and executes the first one it finds. Effect functions might serve another state, print text, or perform some other operation.

Every time a `Command` uses a callback, it passes a reference to its encapsulating state. `Command` effect callbacks can always access and alter the State in which the `Command` was created. When a `State` is made inactive, the `Commands` object and associated references are destroyed.

Static methods in `State` generate callbacks to pass to a `Command` object on creation that evaluate text input. Static methods in `GpioState` evaluate Gpio input.
