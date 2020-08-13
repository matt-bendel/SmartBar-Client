from time import sleep
from nanpy import (ArduinoApi, SerialManager)
import RPi.GPIO as GPIO
import pigpio
import board
import neopixel

GPIO.setmode(GPIO.BCM)
pi = pigpio.pi()

try:
    connection = SerialManager()
    ar = ArduinoApi(connection=connection)
except:
    print("Failed to connect to Arduino.")
    exit()

LED = board.D18
SERVO = 14
SENSOR_PINS = [
        2,
        16,
        12,
        7,
        3,
        8,
        25
    ]
STEP = 21
DIR = 20
CW = 1
CCW = 0

PUMP_PINS = [
        5,
        12,
        11,
        10,
        9,
        8,
        7,
        6
    ]

FSR_PIN = 0

def test_led(led_pin):
    num_pixels = 22
    pixel_pin = led_pin
    order = neopixel.GRB
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=order)
    print("LED Setup")

    print("Off")
    pixels.fill((0, 0, 0))
    pixels.show()
    sleep(3)
    print("Green")
    pixels.fill((0, 255, 0))
    pixels.show()
    sleep(2)
    pixels.fill((255, 0, 0))
    pixels.show()
    sleep(2)
    pixels.fill((0, 0, 255))
    pixels.show()
    sleep(2)
    pixels.fill((255, 128, 0))
    pixels.show()
    sleep(2)
    pixels.fill((0, 0, 0))
    pixels.show()

def test_pumps(pump_pins, a):
    print("Entering Pump Test")
    for pump in pump_pins:
        a.digitalWrite(pump, a.HIGH)
        a.digitalWrite(pump, a.OUTPUT)

    print("Pumps Setup")
    sleep(2)

    for pump in pump_pins:
        print("Pump Pin " + str(pump) + "Pumping")
        a.digitalWrite(pump, a.LOW)
        sleep(0.75)
        a.digitalWrite(pump, a.HIGH)
        sleep(2)

    print("Pump Test Complete")

def test_fsr(fsr_pin, a):
    print("Entering FSR Test, Hit Ctrl C to Leave")
    try:
        while True:
            print("FSR Reading: " + str(a.analogRead(fsr_pin)))
            sleep(1)
    except KeyboardInterrupt:
        print("Exiting FSR Test")

def test_servo(servo_pin, pigpiod):
    print("Servo with 1500 PWM")
    pigpiod.set_servo_pulsewidth(servo_pin, 1500)
    sleep(2)
    print("Servo with 1300 PWM")
    pigpiod.set_servo_pulsewidth(servo_pin, 1300)
    sleep(2)
    print("Servo with 1100 PWM")
    pigpiod.set_servo_pulsewidth(servo_pin, 1100)
    sleep(2)
    print("Back to 1500 PWM")
    pigpiod.set_servo_pulsewidth(servo_pin, 1500)

def test_stepper(step, dir, sensor_pins, cw, ccw, pigpiod):
    print("Entering Stepper and Sensor Test")
    for pin in sensor_pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print("Sensors Setup")
    pigpiod.write(dir, cw)

    for pin in sensor_pins:
        if pin != 2:
            print("Traveling to Pin With GPIO: " + str(pin))
            pigpiod.set_PWM_dutycycle(step, 128)
            pigpiod.set_PWM_frequency(step, 800)
            while not GPIO.input(pin):
                sleep(0.05)
            pigpiod.set_PWM_dutycycle(step, 0)
            pigpiod.set_PWM_frequency(step, 0)
            print("Arrived at Pin")
            sleep(2)

    pigpiod.write(dir, ccw)
    pigpiod.set_PWM_dutycycle(step, 128)
    pigpiod.set_PWM_frequency(step, 800)

    while not GPIO.input(2):
        sleep(0.05)

    pigpiod.set_PWM_dutycycle(step, 0)
    pigpiod.set_PWM_frequency(step, 0)

    print("Back Home, Test Complete")

while True:
    value = input("Enter one of the following numbers to test:\n1: LEDs\n2: Pumps\n3: FSR\n4: Servo\n5: Stepper and Sensors")
    if value == '1':
        test_led(LED)
    elif value == '2':
        test_pumps(PUMP_PINS, ar)
    elif value == '3':
        test_fsr(FSR_PIN, ar)
    elif value == '4':
        test_servo(SERVO, pi)
    elif value == '5':
        test_stepper(STEP, DIR, SENSOR_PINS, CW, CCW, pi)