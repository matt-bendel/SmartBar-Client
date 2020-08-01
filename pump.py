from time import sleep
# from nanpy import (ArduinoApi, SerialManager)
# import RPi.GPIO as GPIO
# import pigpio
from pubsub import pub


# pi = pigpio.pi()

class Pump:
    # position 0 on pin 5
    ON = 1
    OFF = 0
    pin = False
    position_pins = {
        1: 13,
        2: 12,
        3: 11,
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
        # try:
        #     connection = SerialManager()
        #     ar = ArduinoApi(connection=connection)
        # except:
        #     print("Failed to connect to Arduino.")
        # ar.pinMode(13, ar.OUTPUT);
        # ar.pinMode(12, ar.OUTPUT);
        # ar.pinMode(11, ar.OUTPUT);
        # ar.pinMode(10, ar.OUTPUT);
        # ar.pinMode(9, ar.OUTPUT);
        # ar.pinMode(8, ar.OUTPUT);
        # ar.pinMode(7, ar.OUTPUT);
        # ar.pinMode(6, ar.OUTPUT);
        #
        # a = ar;

        self.kill_all_pumps()

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
        # self.a.digitalWrite(13, self.OFF)
        # self.a.digitalWrite(12, self.OFF)
        # self.a.digitalWrite(11, self.OFF)
        # self.a.digitalWrite(10, self.OFF)
        # self.a.digitalWrite(9, self.OFF)
        # self.a.digitalWrite(8, self.OFF)
        # self.a.digitalWrite(7, self.OFF)
        # self.a.digitalWrite(6, self.OFF)
        print("All Pumps Killed")

    def pump(self):
        pub.sendMessage('pump-start')
        print('Current Pump Pin: ' + str(self.pin))
        # self.a.digitalWrite(self.pin, self.ON)

    def stop(self):
        pub.sendMessage('pump-stop')
        for x in self.position_pins:
            pass
            # self.a.digitalWrite(self.position_pins[x], self.OFF)

    def startPump(self, position):
        if position in self.position_pins:
            self.pin = self.position_pins[position]
            self.start_pump = True

    def pumpMixer(self):
        self.pump()
        sleep(3)  # 30 seconds
        self.stop()
