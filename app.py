from time import sleep
from pubsub import pub
from smart_bar import SmartBar
from order_manager import OrderManager
from threading import Thread
import requests

class App:
    def run(self):
        self.setup()
        self.loop()

    def setup(self):
        print("Create App")
        requests.get('http://smart-bar-app.herokuapp.com/api/orders/delete_all')

        pub.subscribe(self.notify, pub.ALL_TOPICS)

        self.order_manager = OrderManager()
        self.smart_bar = SmartBar()

        order_manager_thread = Thread(target = self.order_manager.run, daemon = True)
        order_manager_thread.start()

    def loop(self):
        order = {}

        try:
            while True:
                if not self.smart_bar.isProcessing() and bool(order):
                    pub.sendMessage('order-creating', status='creating')
                    self.smart_bar.processDrink(order["drink"])
                    requests.get('http://smart-bar-app.herokuapp.com/api/orders/delete_all')
                    order = {}
                elif self.smart_bar.isProcessing() == False:
                    order = self.getNewOrder()

                if (self.order_manager.cancel):
                    print(self.order_manager.cancel)
                    self.smart_bar.stop()
                    self.order_manager.cancel = False

                sleep(0.1)

            print("Done making orders")
        except KeyboardInterrupt:
            print ("\nCtrl-C pressed.")
            self.smart_bar.stop()
            GPIO.cleanup()

    def notify(self, topicObj=pub.AUTO_TOPIC, **msgData):
        status = False

        if bool(msgData) and msgData['status']:
            status = msgData['status']

        self.order_manager.queueUpdateOrder(topicObj.getName(), status)
        print('topic "%s": %s' % (topicObj.getName(), msgData))

    def getNewOrder(self):
        return self.order_manager.getLatestOrder()


app = App()
app.run()
