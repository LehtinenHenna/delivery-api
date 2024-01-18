from flask import request
from flask_restful import Resource

class DeliveryFeeResource:

    def post(self):
        '''
        Calculate delivery fee based on parameters in the request.
        POST -> /deliveryfee
        '''
        json_data = request.get_json()
        # Calculate delivery fee based on parameters in json_data, return as {"delivery_fee": 710} with status 200 OK
