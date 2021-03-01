Gpio
____

The `GpioUtil` module provides utility classes for wrapping RPIO/GPIO functionality with the `Rpi.GPIO` library. A `Switch` class gets times that switches were pressed for and sends it to the `GpioState` for execution. The `GpioState` maintains a dictionary of pins and their associated `GpioUtil` objects and will deactivate them on state changes when the lifecycle method `end_state()` is called, which happens when a state is changed.

`GpioStates` contains a general purpose GpioState which extends `StateMachine.States`. It handles inputs such as button presses by creating dictionary input events to pass to `Program.Execute` for use with its `self.Commands`, mirroring how a regular `StateMachine.State` handles text input commands.

`GpioState_10_press` is an example program for a lab which stores 10 variable length button presses. After 10 presses are recorded, it flashes an LED light 10 times for the length of each button press.

An instance of `HitachiDisplay.HitachiPrinter` can be set to Game.Display.printer to use a Hitachi Display for printing game output via 4 bit i2c protocol.
