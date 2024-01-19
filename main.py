from flask import Flask
from flask_restful import Api
from resources.delivery_fee import DeliveryFeeResource

class DeliveryApi:

    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.register_resources()

    def register_resources(self):
        self.api.add_resource(DeliveryFeeResource, '/delivery-fee')

    def run(self):
        self.app.run(debug=True)
    
if __name__ == '__main__':
    delivery_api = DeliveryApi()
    delivery_api.run()