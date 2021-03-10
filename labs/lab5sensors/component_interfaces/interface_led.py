import RPi.GPIO as GPIO

class Led:
    """
    A class for controlling LEDS by changing corresponding GPIO outputs.

    Sets mode to output on initialization
    
    :param pin: A pin wired to from the negative lead of the LED to ground.
    :type pin: int
    
    """
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        """
        Turns off LED by setting GPIO.LOW on `self.pin`
        
        """
        GPIO.output(self.pin, GPIO.LOW)
    
    def on(self):
        """
        Turns on LED by setting GPIO.HIGH on `self.pin`
        
        """
        GPIO.output(self.pin, GPIO.HIGH)
