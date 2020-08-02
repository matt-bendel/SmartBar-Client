from time import sleep
from nanpy import (ArduinoApi, SerialManager)
from pubsub import pub

class WeightSensor:
    FSR_ANALOG = 0
    fsr_reading = 0
    a = False
    glass_placed = False

    def __init__(self):
        try:
            connection = SerialManager()
            ar = ArduinoApi(connection=connection)
        except:
            print("Failed to connect to Arduino.")
            exit()

        self.a = ar
        print("Create WeightSensor")

    def run(self):
        while True:
            val = self.read()
            print("Analog Reading: " + str(val))
            sleep(0.5)

    def read(self):
        value = self.a.analogRead(self.fsr_reading)

        tmp_glass_placed = value >= 150

        if tmp_glass_placed != self.glass_placed:
            self.glass_placed = tmp_glass_placed
            if self.glass_placed:
                pub.sendMessage('glass-placed')
            else:
                pub.sendMessage('glass-removed')

            return value
        else:
            return value
