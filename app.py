from flask import Flask, request, jsonify

class DeliveryApi:

    def __init__(self):
        self.app = Flask(__name__)

    def run(self):
        pass
    
if __name__ == '__main__':
    delivery_api = DeliveryApi()
    delivery_api.run()