from time import sleep
import RPi.GPIO as GPIO
import pigpio
from pubsub import pub
pi = pigpio.pi()
GPIO.setmode(GPIO.BCM)

class StepperMotor:
    current_position = 0
    current_rotation = 1
    destination = 0
    complete = False

    DIRECTION_PIN = 20
    STEP_PIN = 21
    CCW = 0 # Counterclockwise rotation
    CW = 1 # Clockwise rotation
    SENSOR_PINS = [
        2,
        16,
        12,
        7,
        3,
        8,
        25
    ]

    def __init__(self):
        print("Create StepperMotor")
        self.setup()

    def __del__(self):
        self.stop()

    def setup(self):
        print("move")
        # Set up pins as an output
        GPIO.setup(self.DIRECTION_PIN, GPIO.OUT)
        GPIO.setup(self.STEP_PIN, GPIO.OUT)
        self.setupSensor()

    def setupSensor(self):
       for pin in self.SENSOR_PINS:
           GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
           GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.activeSensor, bouncetime=100)
           if not GPIO.input(pin):
               self.current_position = pin
               print(str(self.current_position))

    def activeSensor(self, pin):
        self.current_position = self.SENSOR_PINS.index(pin)
        self.check_route()
        print("sensor" + str(self.current_position))

    def drive(self):
        pub.sendMessage('stepper-drive')
        pi.set_PWM_dutycycle(self.STEP_PIN, 128)
        pi.set_PWM_frequency(self.STEP_PIN, 800)
        pi.write(self.DIRECTION_PIN, self.current_rotation) # Set default direction
        print("drive")
        print("Dir: " + str(self.current_rotation))

    def check_route(self):
        if self.current_position > self.destination:
            self.current_rotation = self.CCW
            self.drive()
        elif self.current_position < self.destination:
            self.current_rotation = self.CW
            self.drive()
        elif self.arrived():
            self.stop()
            pub.sendMessage('stepper-arrived')
        print("Route Check")

    def setDestination(self, destination):
        if destination == 0:
            self.complete = True
        self.destination = destination
        print('Stepper Dest: ' + str(destination) + ' Pin: ' + str(self.SENSOR_PINS[destination]))

    def arrived(self):
        return self.current_position == self.destination

    def stop(self):
        pub.sendMessage('stepper-stop')
        pi.set_PWM_dutycycle(self.STEP_PIN, 0)
        pi.set_PWM_frequency(self.STEP_PIN, 0)

    def listenGlassPlaced(self):
        if self.destination == False:
            self.check_route()