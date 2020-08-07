from stepper_motor import StepperMotor
from servo_motor import ServoMotor
from pump import Pump
from weight_sensor import WeightSensor
from led import Led
from time import sleep
from threading import Thread
from pubsub import pub
import requests

class SmartBar:
    currentDrink = {}
    currentIngredient = {}
    processing = False
    complete = False
    mixer = False
    dispense = True
    canceled = False

    def __init__(self):
        print("Create SmartBar")
        self.stepper_motor = StepperMotor()
        self.servo_motor = ServoMotor()
        self.pump = Pump()
        self.weight_sensor = WeightSensor()
        self.led = Led()
        self.setup()

    def setup(self):
        led_thread = Thread(target = self.led.run, daemon = True)
        led_thread.start()

        weight_sensor_thread = Thread(target = self.weight_sensor.run, daemon = True)
        weight_sensor_thread.start()

        servo_motor_thread = Thread(target = self.servo_motor.run, daemon = True)
        servo_motor_thread.start()

        pump_thread = Thread(target = self.pump.run, daemon = True)
        pump_thread.start()

        pub.subscribe(self.stop, 'glass-removed')
        pub.subscribe(self.lissentArrived, 'stepper-arrived')
        pub.subscribe(self.listenPumpComplete, 'pump-complete')
        pub.subscribe(self.listenDispensComplete, 'dispens-complete')


    def processDrink(self, drink):
        if self.processing:
            return False

        self.processing = True
        self.currentDrink = drink
        self.prepareNextIngredient()
        print("start")

    def prepareNextIngredient(self):
        if self.canceled or not self.currentDrink["ingredients"]:
            self.complete = True
            if not self.mixer:
                self.dispense = False
                self.stepper_motor.setDestination(0)
                self.stepper_motor.check_route()

            while self.stepper_motor.current_position != 0:
                sleep(0.5)

            self.mixer = False
            self.stepper_motor.no_order = True
            requests.get('http://smart-bar-app.herokuapp.com/api/orders/delete_all')
            if not self.canceled:
                pub.sendMessage('order-completed')
            self.processing = False
            self.canceled = False
            return

        self.currentIngredient = self.currentDrink["ingredients"].pop(0)
        if self.currentIngredient["type"] == 'mixer':
            self.mixer = True
            self.stepper_motor.setDestination(0)
            print("TEST TEST TEST")
        else:
            self.stepper_motor.setDestination(self.currentIngredient["position"])

        # if glass is all ready placed check route
        while not self.weight_sensor.glass_placed:
            sleep(0.5)

        self.servo_motor.cancel = False
        self.stepper_motor.no_order = False
        self.stepper_motor.check_route()

    def isProcessing(self):
        return self.processing

    def listenPumpComplete(self):
        self.prepareNextIngredient()

    def listenDispensComplete(self):
        self.prepareNextIngredient()

    def lissentArrived(self):
        if not self.currentIngredient:
            return

        if self.currentIngredient["type"] == "liquor":
            if self.dispense:
                self.servo_motor.startDispens(self.currentIngredient["pivot"]["amount"])
            self.dispense = True
        elif self.currentIngredient["type"] == "mixer":
            self.pump.startPump(self.currentIngredient["position"])

    def stop(self):
        if self.complete:
            self.led.rainbow = False
            sleep(2)
            self.led.red()
            self.complete = False
            return

        pub.sendMessage('order-cancelled')
        requests.get('http://smart-bar-app.herokuapp.com/api/orders/delete_all')
        self.currentDrink = {}
        self.currentIngredient = {}
        self.servo_motor.cancel = True
        self.stepper_motor.stop()
        self.stepper_motor.go_home()
        self.led.rainbow = False
        self.led.red()
        self.pump.stop()
        self.processing = False
        self.canceled = True

