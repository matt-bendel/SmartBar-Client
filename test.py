from time import sleep
from nanpy import (ArduinoApi, SerialManager)
import RPi.GPIO as GPIO
import board
import neopixel

num_pixels = 22
pixel_pin = board.D18
order = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=order)

pixels.fill((0, 0, 0))
pixels.show()
sleep(3)
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


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if order == neopixel.RGB or order == neopixel.GRB else (r, g, b, 0)

def rainbow_cycle(wait = 0.001):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        sleep(wait)


while True:
    rainbow_cycle()
# try:
#     connection = SerialManager()
#     a = ArduinoApi(connection=connection)
# except:
#     print("Failed to connect to Arduino.")
#     exit()
#
# a.digitalWrite(5, a.HIGH)
# a.digitalWrite(12, a.HIGH)
# a.digitalWrite(13, a.HIGH)
# a.digitalWrite(10, a.HIGH)
# a.digitalWrite(9, a.HIGH)
# a.digitalWrite(8, a.HIGH)
# a.digitalWrite(7, a.HIGH)
# a.digitalWrite(6, a.HIGH)
#
#
# a.pinMode(5, a.OUTPUT)
# a.pinMode(12, a.OUTPUT)
# a.pinMode(13, a.OUTPUT)
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
# a.digitalWrite(13, a.LOW)
# sleep(0.75)
# a.digitalWrite(13, a.HIGH)
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

