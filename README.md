# rpio-cli-state-machine

## A library for handling RPi-GPIO events on a Raspberry Pi

The purpose of these classes is to abstract the logic related to responding to hardware or software input and output events by wrapping them in states.

`State`s have a `Commands` object which consists of `Command` objects. Each `Command` has two callbacks. The first callback checks input to see if it meets the condition. The second callback is called if it does. 

Various generator functions, generally static methods of a `State` class, return appropriate callbacks.

Callbacks are passed the `State` where the command was executed and can access the other classes from that state, such as `state_instance.program`

A program that uses RPi-GPIO inputs can be written by extending `GpioState`.



### Created for Systems Fundamentals with Professor Egelstein by Karl Miller, Feb 2021


- run Makefile to build the docs
- i.e. make builder
- where "builder" is one of the supported builders, like html, latex, or linkcheck
