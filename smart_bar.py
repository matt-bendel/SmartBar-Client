from time import sleep
from pubsub import pub
import requests
import serial

class SmartBar:
    currentDrink = {}
    currentIngredient = {}
    processing = False
    mixer = False
    arduino = serial.Serial('/dev/cu.usbmodem14401', 9600, timeout=2)
    sleep(2)

    def __init__(self):
        print("Create SmartBar")
        self.setup()

    def setup(self):
        pub.subscribe(self.arduinoDone, 'arduino-done');

    def processDrink(self, drink):
        if self.processing:
            return False

        print("start")

        while self.arduino.readline().decode('utf-8').rstrip() != 'ready':
            sleep(0.5)

        print("in")
        self.processing = True
        self.currentDrink = drink
        self.arduino.write(b"init\n")
        print("init")
        while self.currentDrink["ingredients"]:
            self.prepareNextIngredient()

        if not self.mixer:
            self.arduino.write(b"0\n")

        self.arduino.write(b"69\n")
        print(str(69))

        val = self.arduino.readline().decode('utf-8').rstrip()
        while val != 'complete':
            print(val)
            val = self.arduino.readline().decode('utf-8').rstrip()

        print("Done")
        pub.sendMessage("arduino-done")

    def prepareNextIngredient(self):
        self.currentIngredient = self.currentDrink["ingredients"].pop(0)
        if self.currentIngredient["type"] == 'mixer' and not self.mixer:
            self.mixer = True
            self.arduino.write(b"0\n")
            position = self.currentIngredient["position"]
            self.arduino.write(bytes(str(position), encoding="utf-8") + b"\n")
        elif self.currentIngredient["type"] == 'mixer' and self.mixer:
            position = self.currentIngredient["position"]
            self.arduino.write(bytes(str(position), encoding="utf-8") + b"\n")
        else:
            position = self.currentIngredient["position"]
            amount = self.currentIngredient["pivot"]["amount"]
            self.arduino.write(bytes(str(position), encoding="utf-8") + b"\n")

            self.arduino.write(bytes(str(amount), encoding="utf-8") + b"\n")
        return


    def isProcessing(self):
        return self.processing

    def arduinoDone(self):
        # requests.get('http://smart-bar-app.herokuapp.com/api/orders/delete_all')

        self.processing = False
        self.mixer = False

        pub.sendMessage("order-complete")

        return

    def stop(self):
        pub.sendMessage('order-cancelled')
        requests.get('http://smart-bar-app.herokuapp.com/api/orders/delete_all')
        print("stop delete")
        self.processing = False
        self.canceled = True

