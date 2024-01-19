from flask import request
from flask_restful import Resource
from http import HTTPStatus

class DeliveryFeeResource(Resource):

    def post(self):
        '''
        Calculate delivery fee based on parameters in the request.
        POST -> /deliveryfee
        '''
        json_data = request.get_json()
        print('json_data', json_data)
        # Calculate delivery fee based on parameters in json_data, return as {"delivery_fee": 710} with status 200 OK
        return {'delivery_fee': 0}, HTTPStatus.OK