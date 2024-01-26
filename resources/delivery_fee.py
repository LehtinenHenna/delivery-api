'''HTTP endpoints related to delivery fee.

Contains classes that inherit from flask_restful.Resource
and define HTTP endpoints for URLs.
'''
from http import HTTPStatus
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from schemas.delivery_fee import DeliveryFeeSchema
from utils.delivery_fee_calculator import DeliveryFeeCalculator


class DeliveryFeeResource(Resource):
    '''
    HTTP endpoints for the URL /delivery-fee.

    ...

    Attributes
    ----------
    delivery_fee_schema: DeliveryFeeSchema
        A marshmallow schema for validating request data
    delivery_fee_calculator: DeliveryFeeCalculator
        Used to calculate the delivery fee based on the request

    Methods
    -------
    post()
        HTTP POST endpoint
    '''

    def __init__(self):
        self.delivery_fee_schema = DeliveryFeeSchema()
        self.delivery_fee_calculator = DeliveryFeeCalculator()

    def post(self):
        '''Calculates delivery fee based on parameters in the request.

        Returns a JSON with the calculated delivery_fee.
        POST endpoint to URL /delivery-fee.
        '''

        request_dict = request.get_json()
        try:
            # Validate the request data with marshmallow
            validated_request_dict = self.delivery_fee_schema.load(data=request_dict)
        except ValidationError as error:
            return {
                'message': 'Validation errors', 'errors': error.messages_dict
            }, HTTPStatus.BAD_REQUEST

        delivery_fee = self.delivery_fee_calculator.calculate_delivery_fee(validated_request_dict)

        return {'delivery_fee': int(delivery_fee)}, HTTPStatus.OK
    