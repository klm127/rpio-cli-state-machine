"""
Utility classes for interfacing with the RPi.GPIO library on a Raspberry Pi.

"""

import time
import RPi.GPIO as GPIO

class Switch:
    """
    A class to wrap a GPIO input event as triggered by a simple switch.
    
    Sets up a GPIO PUD_UP Rising switch and adds a GPIO event handler to it. When the event handler is triggered by a switch event (bouncetime 100ms), it calls :method:`self.press`. Press waits for input to drop, then sends a dictionary to the state containing information about the pin location and the length of the press.

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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback = self.press, bouncetime=100)
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
        print('press event on ' + str(ev)) # prints pin number
        start = time.time()
        while GPIO.input(self.pin) == 0: # another time check here could handle falling bounce times
            pass
        end = time.time()
        self.last_press_time = end-start
        ev = {
            "type": 'button-press',
            "pin": self.pin,
            "length": self.last_press_time
        }
        self.state.execute(ev)

class Led:
    """
    A class for controlling LEDS by changing corresponding GPIO outputs.

    Sets mode to output on initialization
    
    :param pin: A BCM-numbered GPIO pin wired to from the negative lead of the LED to ground.
    :type pin: int
    
    """
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    def on(self):
        """
        Turns on LED by setting GPIO.LOW on `self.pin`
        
        """
        GPIO.output(self.pin, GPIO.LOW)
    
    def off(self):
        """
        Turns off LED by setting GPIO.HIGH on `self.pin`
        
        """
        GPIO.output(self.pin, GPIO.HIGH)

