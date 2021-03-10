"""
States specific to interfacing with pins on a Raspberry PI
"""

from StateMachine import States,Program,Commands
import RPi.GPIO as GPIO
import time

class GpioState(States.InitialState):
    """
    A state for handling GPIO input events

    Changes program state to a mode which handles GPIO events. Clears out inherited commands and creates a new `Commands` object for use with GPIO-based commands.

    Contains a dictionary, `self.pins`, with keys corresponding to pins and values corresponding to objects from `GpioUtil`.

    :param program: A `Program` instance.
    :type program: class Program

    """

    def __init__(self, program):
        States.InitialState.__init__(self, program)
        program.name = '~ State Machine : GPIO Input State ~'
        self.commands = Commands.Commands(self)
        self.pins = {}

    def press_cb(self, pin):
        """
        Returns a callback for use with a `Command` object. That callback tests if an input object's `["pin"]` property is equal to the parameter pin, and returns true if it matches.

        :param pin: The pin an input should be checked against
        :type pin: int
        :returns: A callback passed to a `Command` object as the `bool_func` parameter.
        :rtype: Function

        """
        self.pins[pin] = Switch(self, pin)

        def cb(state, test):
            if test["pin"] == pin:
                return True
            else:
                return False

        return cb

    def execute(self, inp):
        """
        Overwrites inherited method. If it is passed a string input, prints an error message and returns false. Otherwise, checks commands.

        :param inp: An input object
        :type inp: str | Dict
        :returns: True if a matching command was found and input was not a string, false otherwise.
        :rtype boolean:

        """
        b = False
        if type(inp) == str:
            print('String input invalid in GPIO state')
        else:
            b = self.commands.check_commands(inp)
        return b

    @staticmethod
    def print_switch_info(state, inp):
        """
        Debug method passed as a callback to a `Command` object in the `effect` parameter. Prints information about input received.

        :param state: The calling state, passed by the `Command` object.
        :type state: class State
        :param inp: The input object, passed by the `Command` object.
        :type inp: dict

        """
        print('in state: ' + str(state))
        print('input detected:')
        print(str(inp))

class Switch:
    """
    A class to wrap a GPIO input event as triggered by a simple switch.
    
    Sets up a GPIO PUD_UP Rising switch and adds a GPIO event handler to it. When the event handler is triggered by a switch event (bouncetime 100ms), it calls `self.press`. Press waits for input to drop, then sends a dictionary to the state containing information about the pin location and the length of the press.

    :param state: The containing state object.
    :type state: class State
    :param pin: The GPIO pin in BCM numbering which is sending current to the switch.
    :type pin: int

    """
    def __init__(self, state, pin):
        self.state = state
        self.pin = pin
        self.last_press_time = 0
        self.activate()

    def activate(self):
        """
        Called on initialization. Sets mode to GPIO.BCM and calls related GPIO functions to set up the switch. Adds an event detect with GPIO for GPIO.RISING events with a bouncetime of 100.
        
        """
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback = self.press, bouncetime=120)
        GPIO.setwarnings(False)

    def deactivate(self):
        """
        Calls GPIO.remove_event_detect on this pin to deactivate it.
        
        """
        GPIO.remove_event_detect(self.pin)

    def press(self, ev):
        """
        Callback given to GPIO event detector. Gets the length of time the switch is active for, then creates an event dictionary with the following properties:
        
        - 'type': 'button-press'
        - 'pin': an integer corresponding to the BCM pin number the switch is wired to; `self.pin`
        - 'length': A float representing the time in seconds which the switch was active
        
        :param ev: The GPIO pin (BCM) on which a GPIO.RISING edge was detected
        :type ev: int
        
        """
        #  print('press event on ' + str(ev)) # prints pin number
        start = time.time()
        while GPIO.input(self.pin) == 0:
            time.sleep(0.1)
            pass
        end = time.time()
        self.last_press_time = end-start
        ev = {
            "type": 'button-press',
            "pin": self.pin,
            "length": self.last_press_time
        }
        self.state.execute(ev)
