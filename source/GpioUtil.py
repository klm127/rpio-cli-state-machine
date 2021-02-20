import time
import RPi.GPIO as GPIO


class Switch:
    """
    Attached to a switch by a GPIO state

    Sets the switch to 'variable length' whereby every press will be 
    sent to state.program.execute. Tracks length of press and zeros 
    that length when no input detected for end_after seconds.

    Attributes
    ----------
    self.state : State The calling state, a GPIO state
    self.pin : int The pin of the switch, by default, current pin
    self.last_press_time : float The last press time of this switch, not currently used

    Methods
    -------
    self.remove(self) : Removes GPIO event detection for this switch
    self.press(self, ev) : Callback given to GPIO. Figures out press 
     time and builds an object to send to state.execute for comparison
     against commands

    """
    def __init__(self, state, pin):
        self.state = state
        self.pin = pin
        self.last_press_time = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback = self.press, bouncetime=100)
        GPIO.setwarnings(False)

    def remove(self):
        GPIO.remove_event_detect(self.pin)
        print(self)

    def clear_times(self):
        self.times = []
        self.press_length = 0

    def press(self, ev):
        print('press event on ' + str(ev))
        start = time.time()
        while GPIO.input(self.pin) == 0:
            pass
        end = time.time()
        self.last_press_time = end-start
        ev = {
            "type": 'button-press',
            "pin": self.pin,
            "length": self.last_press_time
        }
        self.state.execute(ev)
