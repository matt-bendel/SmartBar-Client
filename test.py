from time import sleep
from nanpy import (ArduinoApi, SerialManager)
import RPi.GPIO as GPIO
# import board
# import neopixel
#
# num_pixels = 21
# pixel_pin = board.D18
# order = neopixel.GRB
# pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False, pixel_order=order)
#
# def blue(selfself):
#     print("green")
#     pixels.fill((0, 0, 255))
#     pixels.show()
#
# sleep(5)
# pixels.fill((0, 0, 0))
# pixels.show()
# exit()

try:
    connection = SerialManager()
    a = ArduinoApi(connection=connection)
except:
    print("Failed to connect to Arduino.")
    exit()

sleep(5)
a.pinMode(2, a.OUTPUT)
a.digitalWrite(2, a.HIGH)
sleep(2)
a.digitalWrite(2, a.LOW)
sleep(0.75)
a.digitalWrite(2, a.HIGH)
# a.digitalWrite(5, a.HIGH)
# a.digitalWrite(12, a.HIGH)
# a.digitalWrite(2, a.HIGH)
# a.digitalWrite(10, a.HIGH)
# a.digitalWrite(9, a.HIGH)
# a.digitalWrite(8, a.HIGH)
# a.digitalWrite(7, a.HIGH)
# a.digitalWrite(6, a.HIGH)
#
#
# a.pinMode(5, a.OUTPUT)
# a.pinMode(12, a.OUTPUT)
# a.pinMode(2, a.OUTPUT)
# a.pinMode(10, a.OUTPUT)
# a.pinMode(9, a.OUTPUT)
# a.pinMode(8, a.OUTPUT)
# a.pinMode(7, a.OUTPUT)
# a.pinMode(6, a.OUTPUT)
#
# sleep(2)
#
# a.digitalWrite(5, a.LOW)
# sleep(0.75)
# a.digitalWrite(5, a.HIGH)
# sleep(2)
# a.digitalWrite(12, a.LOW)
# sleep(0.75)
# a.digitalWrite(12, a.HIGH)
# sleep(2)
# a.digitalWrite(2, a.LOW)
# sleep(0.75)
# a.digitalWrite(2, a.HIGH)
# sleep(2)
# a.digitalWrite(10, a.LOW)
# sleep(0.75)
# a.digitalWrite(10, a.HIGH)
# sleep(2)
# a.digitalWrite(9, a.LOW)
# sleep(0.75)
# a.digitalWrite(9, a.HIGH)
# sleep(2)
# a.digitalWrite(8, a.LOW)
# sleep(0.75)
# a.digitalWrite(8, a.HIGH)
# sleep(2)
# a.digitalWrite(7, a.LOW)
# sleep(0.75)
# a.digitalWrite(7, a.HIGH)
# sleep(2)
# a.digitalWrite(6, a.LOW)
# sleep(0.75)
# a.digitalWrite(6, a.HIGH)

