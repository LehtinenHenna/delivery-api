'''Flask server.

This file contains the class DeliveryApi,
which starts and runs a Flask server.
'''
from flask import Flask
from flask_restful import Api
from resources.delivery_fee import DeliveryFeeResource

class DeliveryApi:
    '''Creates a Flask server.'''

    def __init__(self):
        '''Initializes the Flask server.'''

        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.register_resources()

    def register_resources(self):
        '''Adds HTTP endpoints to the API.'''

        self.api.add_resource(DeliveryFeeResource, '/delivery-fee')

    def run(self):
        '''Runs the Flask server.'''

        self.app.run(debug=True)

if __name__ == '__main__':
    delivery_api = DeliveryApi()
    delivery_api.run()
