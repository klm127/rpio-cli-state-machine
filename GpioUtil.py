from datetime import *


class LongSwitch:
    def __init__(self, state, pin, rise, end_after):
        self.state = state
        self.pin = pin
        self.rise = rise
        self.end_after = end_after
        self.press_length = 0
        self.times = []
        # call gpio add event detect - send the press method for callback

    def remove(self):
        # call gpio remove event detect
        print(self)

    def clear_times(self):
        self.times = []
        self.press_length = 0

    def press(self):
        now = datetime.now()
        if len(self.times) != 0:
            since_last = now - self.times[-1]
            if since_last.total_seconds * 1000 > self.end_after:
                self.clear_times()
        self.times.append(now)
        self.press_length = now - self.times[-1]
        ev = {
            "type": 'button-press',
            "pin": self.pin,
            "length": self.press_length
        }
        self.state.execute(ev)


def get_sim_gpio(string):
    ar = string.split(' ')
    sim_command = {
        'type': 'button-press',
        'pin': 0,
        'length': 0
    }
    if len(ar) >= 3:
        try:
            int(ar[1])
            sim_command.pin = ar[1]
            float(ar[2])
            sim_command.length = ar[2]
        except ValueError:
            return sim_command
        return sim_command
