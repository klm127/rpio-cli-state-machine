Usage - StateMachine
--------------------

To run a program using this library, an instance of `Program` is created. As of now, if you wish to add an additional `State`, you need to add functionality to `InitialState` that will serve your new State. In the next iteration, it will be possible to pass `Program` a different initial state on construction.

.. code-block:: Python

    from Program import Program

    program = Program()

    program.execute('gpio-10-press 21 19')

When the above executes, this is what happens:

1. Program is initialized and sets its `State` to a new instance of `InitialState`.

2. When `InitialState` is constructed, it adds `Command` objects to its `Commands` member.

.. code-block:: Python

    class InitialState(State)
        def __init__(self, program):
            State.__init__(self, program)
            self.commands.add(Command(self, State.get_check_string_cb("cli-mode"), State.send_text_state, 'cli-mode'))
            self.commands.add(Command(self, State.get_front_check_string_cb("gpio-10-press"), State.send_gpio_10_press,'gpio-10-press'))


3. The command object is given three arguments. 
    1. The `State` where it was created.
    2. The callback to evaluate input against, e.g. the function returned by `State.get_front_check_string_cb("gpio-10-press")`.
    3. The callback to call if the first callback evaluates to true, e.g. `State.send_gpio_10_press`.

4. `Program.execute` is called with the parameter 'gpio-10-press 21 19'
   
5. `Program.execute` calls `self.state.execute` with this parameter, causing the `InitialState` instance to evaluate that string.

6. When `InitialState` receives the input, it starts checking it against its commands. Each `Command` calls its evalution callback to see if the input meets its conditions.

7. A match is found by the `Command` that received the callback which checks the front part of the string to see if it starts with "gpio-10-press".

8. The `Command` calls the static method `State.send_gpio_10_press` and passes it the instance of `InitialState` and the input string as a parameter.

9. `send_gpio_10_press` parses the input string to see if has trailing parameters that it may pass to the new instance of `GpioState_10_Press` it is about to construct.

10. `send_gpio_10_press` constructs a new instance of `GpioState_10_Press` and gives it those parameters or default parameters if the input was invalid. 

11. `send_gpio_10_press` looks at the `State` parameter that was given to it and finds the reference to `Program`. It sets `Program.state` to the new state.

12. `send_gpio_10_press` calls `end_state` on the old state, closing it out.