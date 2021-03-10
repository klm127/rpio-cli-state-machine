# general libraries
import RPi.GPIO as GPIO
import time
import threading

# state Machine functionality
from StateMachine import States, Program, Commands, GpioStates

Command = Commands.Command

# component wrapping classes
from component_interfaces.interface_hcsr04 import HCSR04_Interface
from component_interfaces.interface_HD44780U import HD44780U_Interface
from component_interfaces.interface_led import Led

DISTANCE_STORE_SIZE = 4
VELOCITY_STORE_SIZE = int(DISTANCE_STORE_SIZE/2)
ACCELERATION_STORE_SIZE = int(DISTANCE_STORE_SIZE/4)

BRAKE_POWER = 100  # for crash mode, how much the "vehicle" can decelerate

class VelocityState(GpioStates.GpioState):
    def __init__(self, program):
        GpioStates.GpioState.__init__(self, program)
        program.name = "~ Velocity Computer ~"
        GPIO.setmode(GPIO.BCM)
        # initialized to 0 until attached
        self.display = 0
        self.ultrasonic_sensor = 0
        self.button = 0
        self.indicator_led = 0
        # display_category indicates what info should be displayed
        self.display_categories = ["crash mode", "distance","velocity","acceleration"]
        self.display_category_index = 0
        # sub-state flags
        self.running = False
        self.isCrashed = False
        self.brake_power = BRAKE_POWER
        # for calculations
        self.distance_matrix = [0] * DISTANCE_STORE_SIZE
        self.time_matrix = [0] * DISTANCE_STORE_SIZE
        self.velocity_matrix = [0] * VELOCITY_STORE_SIZE
        self.velocity_time_matrix = [0] * VELOCITY_STORE_SIZE
        self.acceleration_matrix = [0] * ACCELERATION_STORE_SIZE
        self.acceleration_time_matrix = [0] * ACCELERATION_STORE_SIZE
        self.index = 0
        # threads for running the display and sensor seperately
        self.ultrasonic_thread = 0
        self.display_thread = 0

    def attach_display(self):
        self.display = HD44780U_Interface()
        self.pins[2] = self.display
        self.pins[3] = "HD44780 Display SCL"

    def attach_ultrasonic_sensor(self, trigger, echo):
        self.ultrasonic_sensor = HCSR04_Interface(trigger,echo)
        self.pins[echo] = self.ultrasonic_sensor
        self.pins[trigger] = "HCSR04 Trigger"

    def attach_led(self, pin):
        self.indicator_led = Led(pin)
        self.pins[pin] = self.indicator_led
        self.indicator_led.off()

    def attach_switch(self, pin):
        """
        To the collection of commands, add a command tying a button press to changing flags.
        :param pin: The GPIO pin wired to the switch
        :type pin: int
        """
        self.commands.add(Command(self, self.press_cb(pin), VelocityState.button_substate_change))

    def print(self, text):
        """
        If display is attached, prints to display. Otherwise, console.
        """
        if self.display != 0:
            rows = text.split('\n')
            if len(rows) < 2:
                rows.append(' ')
            self.display.print(rows)
        else:
            print(text)

    def run(self):
        self.running = True
        if self.isCrashed:
            self.display_category_index = self.display_categories.index('crash mode')
            self.isCrashed = False
            if self.indicator_led != 0:
                self.indicator_led.off()
        
        def ultrasonic_thread_cb(state):
            def cb():
                while state.running and not state.isCrashed:
                    state.time_matrix[state.index] = time.time()
                    state.distance_matrix[state.index] = int(100*state.ultrasonic_sensor.read())/100
                    state.calculate()
                    if state.index == DISTANCE_STORE_SIZE - 1:
                        state.index = 0
                    else:
                        state.index += 1
                    time.sleep(0.25)
            return cb

        def display_thread_cb(state):
            def cb():
                while state.running:
                    time.sleep(0.25)
                    state.display_substate()
            return cb
                    
        self.ultrasonic_thread = threading.Thread(target=ultrasonic_thread_cb(self), daemon=True)
        self.ultrasonic_thread.start()
        time.sleep(1)
        self.display_thread = threading.Thread(target=display_thread_cb(self), daemon=True)
        self.display_thread.start()

    def calculate(self):
        last_value_index = self.index - 1
        if last_value_index < 0:
            last_value_index = DISTANCE_STORE_SIZE + last_value_index
        d_1 = self.distance_matrix[last_value_index]
        if d_1 == 0:
            return
        t_1 = self.time_matrix[last_value_index]
        d_2 = self.distance_matrix[self.index]
        t_2 = self.time_matrix[self.index]

        velocity_index = int(self.index/2)
        v_2 = self.velocity_matrix[velocity_index] = (d_2 - d_1)/(t_2 - t_1)
        vt_2 = self.velocity_time_matrix[velocity_index] = (t_2 + t_1)*0.5
        
        self.velocity_matrix[velocity_index] = v_2
        self.velocity_time_matrix[velocity_index] = vt_2

        last_velocity_index = velocity_index - 1
        if last_velocity_index < 0:
            last_velocity_index = VELOCITY_STORE_SIZE + last_velocity_index

        v_1 = self.velocity_matrix[last_velocity_index]
        vt_1 = self.velocity_time_matrix[last_velocity_index]

        a = (v_2 - v_1)/(vt_2 - vt_1)
        at = (vt_2 + vt_1)/2

        acceleration_index = int(self.index/4)
        if(acceleration_index >= ACCELERATION_STORE_SIZE):
            acceleration_index = 0
        self.acceleration_matrix[acceleration_index] = a
        self.acceleration_time_matrix[acceleration_index] = at

    def display_substate(self):
        display_type = self.display_categories[self.display_category_index]
        out_string = display_type
        if display_type == "distance":
            d = VelocityState.average(self.distance_matrix)
            out_string += f">\n {d:.2f} cm"
        elif display_type == "velocity":
            v = VelocityState.average(self.velocity_matrix)
            out_string += f">\n {v:.2f} cm/s"
        elif display_type == "acceleration":
            a = VelocityState.average(self.acceleration_matrix)
            out_string += f" >\n {a:.2f} cm/s^2"
        elif display_type == "crash mode":
            d = VelocityState.average(self.distance_matrix)
            v = (-1) * VelocityState.average(self.velocity_matrix)
            a = (-1) * VelocityState.average(self.acceleration_matrix)
            a = a + self.brake_power
            out_string += f">accl: {a:.2f} "
            t = -v/a
            out_string += f"\nimpct: {t:.2f} "
            if t > 0:
                dist = (0.5 * a * t * t) + v * t + d
                out_string += f"dst: {dist:.2f} "
                if dist > d:
                    self.crash()
            
        if self.running:
            self.print(out_string)

    def crash(self):
        self.isCrashed = True
        if self.indicator_led != 0:
            self.indicator_led.on()
        self.print('--** CRASH **--')
        self.running = False

    def end_program(self):
        print('Goodbye')
        self.running = False
        self.isCrashed = False
        if self.ultrasonic_thread != 0:
            self.ultrasonic_thread.join()
        if self.display_thread != 0:
            self.display_thread.join()

    @staticmethod
    def average(matrix):
        sum = 0
        for i in range(0, len(matrix)):
            sum += matrix[i]
        return sum / len(matrix)
    
    @staticmethod
    def button_substate_change(state, inp):
        if inp['length'] > 1.6:
            state.end_program()
            return
        elif inp['length'] > 0.2:
            if not state.running:
                display_string = "Starting: "
                if state.ultrasonic_sensor == 0:
                    display_string += "No sensor! "
                if state.indicator_led == 0:
                    display_string += "No LED! "
                if state.display == 0:
                    display_string += "No display! "
                state.print(display_string)
                if state.display != 0:
                    time.sleep(1.5)
                if state.ultrasonic_sensor == 0:
                    state.print('Attach ultrasonic sensor.')
                else:
                    state.run()
            else:
                state.display_category_index += 1
                if state.display_category_index >= len(state.display_categories):
                    state.display_category_index = 0
                    


vprogram = Program.Program()
vstate = VelocityState(vprogram)
vstate.attach_switch(25)
vstate.attach_ultrasonic_sensor(5,26) # trigger, echo
vstate.attach_display()
vstate.attach_led(21)
vprogram.load_state(vstate)
        
        
