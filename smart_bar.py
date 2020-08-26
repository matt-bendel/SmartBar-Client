from time import sleep
from pubsub import pub
import requests
import serial

class SmartBar:
    currentDrink = {}
    currentIngredient = {}
    processing = False
    mixer = False
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=2)

    def __init__(self):
        print("Create SmartBar")
        self.setup()

    def setup(self):
        pub.subscribe(self.arduinoDone, 'arduino-done');

    def processDrink(self, drink):
        if self.processing:
            return False

        print("start")

        self.processing = True
        self.currentDrink = drink
        self.arduino.write(b"init\n")
        while self.currentDrink["ingredients"]:
            self.prepareNextIngredient()
        self.arduino.write(b"69\n")

        while self.arduino.readline().decode('utf-8').rstrip() != 'complete':
            sleep(0.5)

        pub.sendMessage("arduino-done")

    def prepareNextIngredient(self):
        self.currentIngredient = self.currentDrink["ingredients"].pop(0)
        if self.currentIngredient["type"] == 'mixer' and not self.mixer:
            self.mixer = True
            self.arduino.write(b"0\n")
            position = self.currentIngredient["position"]
            self.arduino.write(position)
        elif self.currentIngredient["type"] == 'mixer' and self.mixer:
            position = self.currentIngredient["position"]
            self.arduino.write(position)
        else:
            position = self.currentIngredient["position"]
            amount = self.currentIngredient["amount"]
            self.arduino.write(position)
            self.arduino.write(amount)
        return


    def isProcessing(self):
        return self.processing

    def arduinoDone(self):
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

