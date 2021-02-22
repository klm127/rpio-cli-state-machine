.. rpio-cli-state-machine documentation master file, created by
   sphinx-quickstart on Sat Feb 20 19:28:28 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rpio-cli-state-machine
==================================================

`rpio-cli-state-machine` provides classes for managing states in a Python program. Custom states are created by extending `TextInputState`, for cli based programs, or `GpioState`, for programs utilizing the RPIO pins of a Raspberry Pi. 

Each `State` creates `Commands` on initialization, and adds `Command` objects to it. A `Command` consists of two callbacks; a function to test whether a condition is true and a function to execute if it is true. When `State.execute(input)` is called, it checks its Commands for any Commands whose condition matches the input and executes the first one it finds. Effect functions might serve another state, print text, or perform some other operation.

Every time a `Command` uses a callback, it passes a reference to its encapsulating state. `Command` effect callbacks can always access and alter the State in which the `Command` was created. When a `State` is made inactive, the `Commands` object and associated references are destroyed.

The `GpioUtil` module provides utility classes for wrapping RPIO/GPIO functionality with the `Rpi.GPIO` library. A `Switch` class gets times that switches were pressed for and sends it to the `GpioState` for execution. The `GpioState` maintains a dictionary of pins and their associated `GpioUtil` objects and will deactivate them on state changes when the lifecycle method `end_state()` is called, which happens when a state is changed.

Static methods in `State` generate callbacks to pass to a `Command` object on creation that evaluate text input. Static methods in `GpioState` evaluate Gpio input.

.. toctree::
   :maxdepth: 2
   
   about
   usage


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
