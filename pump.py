from time import sleep
from nanpy import (ArduinoApi, SerialManager)
import RPi.GPIO as GPIO
import pigpio
from pubsub import pub


pi = pigpio.pi()

class Pump:
    # position 0 on pin 5
    ON = 0
    OFF = 1
    pin = False
    position_pins = {
        1: 5,
        2: 12,
        3: 2,
        4: 10,
        5: 9,
        6: 8,
        7: 7,
        8: 6
    }
    start_pump = False
    a = False



    def __init__(self):
        print("Create Pump")
        try:
            connection = SerialManager()
            ar = ArduinoApi(connection=connection)
        except:
            print("Failed to connect to Arduino.")
            exit()

        self.a = ar

        self.kill_all_pumps()

        self.a.pinMode(5, self.a.OUTPUT)
        self.a.pinMode(12, self.a.OUTPUT)
        self.a.pinMode(2, self.a.OUTPUT)
        self.a.pinMode(10, self.a.OUTPUT)
        self.a.pinMode(9, self.a.OUTPUT)
        self.a.pinMode(8, self.a.OUTPUT)
        self.a.pinMode(7, self.a.OUTPUT)
        self.a.pinMode(6, self.a.OUTPUT)


    def __del__(self):
        self.stop()

    def run(self):
        while True:
            if self.start_pump:
                self.pumpMixer()
                self.start_pump = False
                pub.sendMessage('pump-complete')
            sleep(0.5)

    def kill_all_pumps(self):
        self.a.digitalWrite(5, self.OFF)
        self.a.digitalWrite(12, self.OFF)
        self.a.digitalWrite(13, self.OFF)
        self.a.digitalWrite(10, self.OFF)
        self.a.digitalWrite(9, self.OFF)
        self.a.digitalWrite(8, self.OFF)
        self.a.digitalWrite(7, self.OFF)
        self.a.digitalWrite(6, self.OFF)
        print("All Pumps Killed")

    def pump(self):
        pub.sendMessage('pump-start')
        print('Current Pump Pin: ' + str(self.pin))
        self.a.digitalWrite(self.pin, self.ON)

    def stop(self):
        pub.sendMessage('pump-stop')
        for x in self.position_pins:
            self.a.digitalWrite(self.position_pins[x], self.OFF)

    def startPump(self, position):
        if position in self.position_pins:
            self.pin = self.position_pins[position]
            self.start_pump = True

    def pumpMixer(self):
        self.pump()
        sleep(3)  # 30 seconds
        self.stop()
