# rpio-cli-state-machine

A libary I am building for accomplishing various Raspberry PI projects.

Currently consists of three modules:
 - StateMachine : for managing program states and user commands
 - Gpio : for interfacing with devices through a Raspberry PI 3b's GPIO pins
 - Game : A text game for display on a Hitachi HD44780 display (or console for debugging) where the user controls a custom character and runs through a maze.
 
## Documentation

[Documentation](https://www.quaffingcode.com/rpio-cli-state-machine/index.html)

Documentation is auto-generated with Sphinx autodoc from in-code docstrings. As I expand on this library, I'll keep it as up to date as possible, at the very least, for my own reference.
 
## State Machine Description

The purpose of State Machine classes is to abstract the logic related to responding to hardware or software input and output events by wrapping them in states.

`State`s have a `Commands` object which consists of `Command` objects. Each `Command` has two callbacks. The first callback checks input to see if it meets the condition. The second callback is called if it does. 

Various generator functions, generally static methods of a `State` class, return appropriate callbacks.

Callbacks are passed the `State` where the command was executed and can access the other classes from that state, such as `state_instance.program`

A program that uses RPi-GPIO inputs can be written by extending `GpioState` in `GpioStates`.

## Game Description


Needs pynput.keyboard for game

## Documentation

[Documentation](https://www.quaffingcode.com/rpio-cli-state-machine/index.html)

### Created for Systems Fundamentals with Professor Egelstein by Karl Miller, Feb 2021

For docs:

- run `sphinx-doc/make.bat` with Sphinx on the path


