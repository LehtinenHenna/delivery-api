from flask import request
from flask_restful import Resource
from http import HTTPStatus

class DeliveryFeeResource(Resource):

    def post(self):
        '''
        Calculate delivery fee based on parameters in the request.
        POST -> /deliveryfee
        '''
        request_dict = request.get_json()
        print('type(request_dict)', type(request_dict))
        
        # Validate request data
        required_keys = (
            "cart_value", 
            "delivery_distance", 
            "number_of_items", 
            "time"
        )
        for key in required_keys:
            if key not in request_dict:
                return {"message": "One or more required keys missing from the request. Required keys: {}".format(required_keys)}
        
        # Calculate delivery fee based on parameters in json_data, return as {"delivery_fee": 710} with status 200 OK
        delivery_fee = 0
            
        return {'delivery_fee': delivery_fee}, HTTPStatus.OK