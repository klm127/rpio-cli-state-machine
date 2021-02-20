import time
import RPi.GPIO as GPIO


class LongSwitch: # contains logic for variable length button presses
    def __init__(self, state, pin, rise=GPIO.RISING, pull=GPIO.PUD_UP,end_after = 50):
        self.state = state
        self.pin = pin
        self.rise = rise # rise and pull depend on how switch was wired
        self.pull = pull
        self.end_after = end_after # how long without input before times are cleared
        self.press_length = 0
        self.times = []
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.press)
        GPIO.setwarnings(False)

    def remove(self):
        GPIO.remove_event_detect(self.pin)
        print(self)

    def clear_times(self):
        self.times = []
        self.press_length = 0

    def press(self, ev):
        print('press event' + str(ev))
        now = time.time()
        if len(self.times) > 0:
            since_last = now - self.times[-1]
            print(since_last)
            print(self.end_after)
            if since_last > self.end_after:
                self.clear_times()
        self.times.append(now)
        self.press_length = now - self.times[0]
        ev = {
            "type": 'button-press',
            "pin": self.pin,
            "length": self.press_length
        } # button presses generate this type of object
        self.state.execute(ev) # state will do something if this object meets a command condition


def get_sim_gpio(string): # converts "sim 1 1000" to a 1 second input on pin 1
    ar = string.split(' ')
    sim_command = {
        'type': 'button-press', # GPIO inputs produce this kind of object
        'pin': 0,
        'length': 0
    }
    if len(ar) >= 3:
        try:
            sim_command['pin'] = int(ar[1])
            sim_command['length'] = float(ar[2])
        except ValueError:
            print('error parsing sim')
            # returns a 0 length button press on pin 0 if sim command can't parse
    return sim_command
