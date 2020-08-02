from stepper_motor import StepperMotor
from servo_motor import ServoMotor
from pump import Pump
from weight_sensor import WeightSensor
from led import Led
from time import sleep
from threading import Thread
from pubsub import pub
import requests
import board
import neopixel

class SmartBar:
    currentDrink = {}
    currentIngredient = {}
    processing = False

    def __init__(self):
        print("Create SmartBar")
        self.num_pixels = False
        self.pixel_pin = board.D23
        self.pixel_order = neopixel.GRB
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=0.05, auto_write=False, pixel_order=self.order)
        self.stepper_motor = StepperMotor()
        self.servo_motor = ServoMotor()
        self.pump = Pump()
        self.weight_sensor = WeightSensor()
        self.led = Led()
        self.setup()

    def setup(self):
        # self.rainbow_cycle()
        #
        # led_thread = Thread(target = self.led.run, daemon = True)
        # led_thread.start()

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
        if not self.currentDrink["ingredients"]:
            requests.get('http://smart-bar-app.herokuapp.com/api/orders/delete_all')
            pub.sendMessage('order-completed', status='completed')
            self.processing = False

            return

        self.currentIngredient = self.currentDrink["ingredients"].pop(0)
        if self.currentIngredient["type"] == 'mixer':
            self.stepper_motor.setDestination(0)
        else:
            self.stepper_motor.setDestination(self.currentIngredient["position"])

        # self.stepper_motor.check_route()
        # if glass is all ready placed check route

        if self.weight_sensor.glass_placed:
            self.stepper_motor.check_route()

    def isProcessing(self):
        return self.processing

    def listenPumpComplete(self):
        self.prepareNextIngredient()

    def listenDispensComplete(self):
        self.prepareNextIngredient()

    def lissentArrived(self):
        if self.currentIngredient["type"] == "liquor":
            self.servo_motor.startDispens(self.currentIngredient["pivot"]["amount"])
        elif self.currentIngredient["type"] == "mixer":
            self.pump.startPump(self.currentIngredient["position"])

    def stop(self):
        pub.sendMessage('order-cancelled', status='cancelled')
        # self.led.orange()
        self.stepper_motor.stop()
        self.servo_motor.stop()
        self.pump.stop()
        self.processing = False

    def rainbow_cycle(self, wait=0.001):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            sleep(wait)

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b) if self.pixel_order == neopixel.RGB or self.pixel_order == neopixel.GRB else (r, g, b, 0)
