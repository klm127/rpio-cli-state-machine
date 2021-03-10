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
        self.reading = False
        self.last_read = 0

    def read(self):
        """
        Runs a thread to get the read. Thread will result in this instance having self.last_read
        set to the distance in cm.
        """
        if not self.reading:
            self.reading = True
            readthread = threading.Thread(target=HCSR04_Interface.getReaderCb(self), daemon=False)
            readthread.start()
        else:
            raise Exception('Read already in progress')

    @staticmethod 
    def getReaderCb(hcs):
        """
        Gets reader thread for use with read
        :param hcs: The ultrasonic reader object
        :class hcs: class extends HCSR04_Interface
        """
        def cb():
            hcs.reading = True
            # send the trigger
            GPIO.output(hcs.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(hcs.trigger_pin, GPIO.LOW)
            safety_start = time.time()
            start = 0
            end = 0
            while 0 == GPIO.input(hcs.echo_pin) and hcs.reading == True:
                start = time.time()
                if(start - safety_start > 3):
                    hcs.reading = False
                    hcs.functional = False
                    raise Exception('too long to read')
            while 1 == GPIO.input(hcs.echo_pin) and hcs.reading == True:
                end = time.time()
                if end - start > 4:
                    hcs.reading = False
                    hcs.functional = False
                    raise Exception('too long to read')
            total_time = end - start
            hcs.last_read = (total_time * 33120.0) / 2
            hcs.reading = False
        return cb
            
            
            
        
