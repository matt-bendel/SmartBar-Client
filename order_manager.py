import requests
from time import sleep

class OrderManager:
    url = ''
    orders = []
    updates = []
    order = {}
    cancel = False

    def __init__(self):
        self.setup()

    def setup(self):
        print("Create OrderManager")

        self.url = 'http://smart-bar-app.herokuapp.com/api/orders'

    def run(self):
        while True:
            # process updates
            # updatesates = self.updates
            # self.updates = []
            #
            # for update in updates:
            #     self.updateOrder(update['message'], update['status'], update['order-id'])

            # fetch latest orders
            self.getOrders()

            sleep(1)

    def getOrders(self):
        r = requests.get(self.url)

        if r.status_code == requests.codes.ok:
            self.orders = r.json()['orders']
            self.cancel = r.json()['cancel-current']
            requests.get('http://smart-bar-app.herokuapp.com/api/orders/delete_all')

    def queueUpdateOrder(self, message, status = False):
        if bool(self.order):
            self.updates.append({'message': message, 'status': status, 'order-id': self.order['id']})
        else:
            print("NO order, status: " + message)

    def updateOrder(self, message, status, order_id):
        data = {
            'message': message
        }

        if status != False:
            data['status'] = status

        print("order manager delete")

    def getLatestOrder(self):
        if self.order:
            self.order = {}

        if self.orders:
            self.order = self.orders.pop()

        return self.order