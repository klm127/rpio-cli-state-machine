import time
import RPi.GPIO as GPIO
import threading


class HCSR04_Interface:
    """
    For interfacing with an ultrasonic sensor.

    GPIO numbering mode should be set in calling scope.

    
    :param trigger_pin: The GPIO pin to transmit trigger signal
    :type trigger_pin: int
    :param echo_pin: The GPIO pin where echo will be received
    :type echo_pin: int
    """
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trigger_pin, GPIO.LOW)
        self.functional = True

    def read(self):
        """
        Reads distance by sending trigger, then waiting for response
        By calculating time of response, determines the distance

        :returns: distance in cm
        :rtype: float
        """
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, GPIO.LOW)
        safety_start = time.time()
        start = time.time()
        end = time.time()
        while 0 == GPIO.input(self.echo_pin):
            start = time.time()
            if(start - safety_start > 3 ):
                raise Exception('too long to read start')
        while 1 == GPIO.input(self.echo_pin):
            end = time.time()
            if (end - start) > 5:
                raise Exception(f'too long to read end {end}... start is {start}')
        total_time = end - start
        return (total_time * 33120.0) / 2
            
            
            
        
