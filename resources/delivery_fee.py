from datetime import datetime, time
from dateutil import parser
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from marshmallow import ValidationError
from math import ceil
from schemas.delivery_fee import DeliveryFeeSchema

delivery_fee_schema = DeliveryFeeSchema()

class DeliveryFeeResource(Resource):

    def __init__(self):
        self.cart_value_free_delivery_limit_cents = 20000
        self.cart_value_surcharge_limit_cents = 1000
        self.number_of_items_surcharge_limit = 4
        self.number_of_items_surcharge_fee_cents = 50
        self.number_of_items_bulk_limit = 12
        self.number_of_items_bulk_fee_cents = 120
        self.delivery_distance_start_meters = 1000
        self.delivery_distance_start_fee_cents = 200
        self.delivery_distance_additional_block_meters = 500
        self.delivery_distance_additional_block_fee_cents = 100
        self.time_rush_weekday = 4 # Monday... Sunday = 0... 6
        self.time_rush_start_hour = time(hour = 15)
        self.time_rush_end_hour = time(hour = 19)
        self.time_rush_multiplier = 1.2
        self.max_delivery_fee = 1500

    def calculate_delivery_distance_fee(self, delivery_fee, delivery_distance):
        delivery_fee += 200
        if delivery_distance >= self.delivery_distance_start_meters:
            delivery_distance -= self.delivery_distance_start_meters
        else:
            delivery_distance = 0
        number_of_additional_distance_blocks = ceil(delivery_distance / self.delivery_distance_additional_block_meters)
        delivery_fee += number_of_additional_distance_blocks * self.delivery_distance_additional_block_fee_cents
        return delivery_fee

    def calculate_number_of_items_fee(self, delivery_fee, number_of_items):
        if number_of_items > self.number_of_items_surcharge_limit:
            number_of_surcharges = number_of_items - self.number_of_items_surcharge_limit
            delivery_fee += number_of_surcharges * self.number_of_items_surcharge_fee_cents
        if number_of_items > self.number_of_items_bulk_limit:
            delivery_fee += self.number_of_items_bulk_fee_cents
        return delivery_fee
    
    def calculate_cart_value_fee(self, delivery_fee, cart_value):
        if cart_value < self.cart_value_surcharge_limit_cents:
            delivery_fee += self.cart_value_surcharge_limit_cents - cart_value
        elif cart_value >= self.cart_value_free_delivery_limit_cents:
            delivery_fee = 0
        return delivery_fee

    def calculate_time_fee(self, delivery_fee, time):
        time_as_datetime = parser.parse(time)
        day_of_the_week = datetime.weekday(time_as_datetime)
        if day_of_the_week == self.time_rush_weekday:
            if self.time_rush_start_hour < time_as_datetime.time() < self.time_rush_end_hour:
                delivery_fee *= self.time_rush_multiplier
        return delivery_fee
    
    def check_max_delivery_fee(self, delivery_fee):
        if delivery_fee > self.max_delivery_fee:
            delivery_fee = self.max_delivery_fee
        return delivery_fee
    
    def post(self):
        '''
        Calculate delivery fee based on parameters in the request.
        POST -> /delivery-fee
        '''
        request_data = request.get_json()
        try:
            delivery_data = delivery_fee_schema.load(data=request_data)
        except ValidationError as error:
            return {'message': 'Validation errors', 'errors': error.messages_dict}, HTTPStatus.BAD_REQUEST
        delivery_fee_functions = {
            self.calculate_delivery_distance_fee: 'delivery_distance',
            self.calculate_number_of_items_fee: 'number_of_items',
            self.calculate_cart_value_fee: 'cart_value',
            self.calculate_time_fee: 'time',
        }
        print('data', delivery_data)
        delivery_fee = 0
        for function, key_name in delivery_fee_functions.items():
            delivery_fee = function(delivery_fee, delivery_data[key_name])
        delivery_fee = self.check_max_delivery_fee(delivery_fee)    
        return {'delivery_fee': int(delivery_fee)}, HTTPStatus.OK