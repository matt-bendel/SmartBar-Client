from time import sleep
import board
import neopixel
from pubsub import pub

class Led:
    num_pixels = 16
    rainbow = False

    def __init__(self):
        print("Create Led")
        self.pixel_pin = board.D18
        self.order = neopixel.GRB
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=0.05, auto_write=False, pixel_order=self.order)
        self.red()

        pub.subscribe(self.green, 'glass-placed')
        pub.subscribe(self.red, 'glass-removed')
        pub.subscribe(self.white, 'stepper-drive')
        pub.subscribe(self.blue, 'stepper-arrived')
        pub.subscribe(self.rainbow, 'order-completed')

    def __del__(self):
        self.stop()

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
        return (r, g, b) if self.order == neopixel.RGB or self.order == neopixel.GRB else (r, g, b, 0)

    def rainbow_cycle(self, wait = 0.001):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            sleep(wait)

    def orange(self):
        print("orange")
        self.pixels.fill((255, 155, 0))
        self.pixels.show()

    def red(self):
        print("red")
        self.pixels.fill((255, 0, 0))
        self.pixels.show()

    def white(self):
        print("white")
        self.pixels.fill((255, 255, 255))
        self.pixels.show()

    def green(selfself):
        print("green")
        self.pixels.fill((0, 255, 0))
        self.pixels.show()

    def blue(selfself):
        print("green")
        self.pixels.fill((0, 0, 255))
        self.pixels.show()

    def run(self):
        while True:
            if (self.rainbow):
                print("test rainbow")
                self.rainbow_cycle(0.0005) # rainbow cycle with 1ms delay per step
            sleep(1)

    def stop(self):
        print("stop led")
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def showRainBow(self):
        self.rainbow = True
