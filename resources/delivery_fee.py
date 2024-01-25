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
    '''HTTP endpoints for the URL /delivery-fee.'''

    def __init__(self):
        self.cart_value_free_delivery_limit_cents = 20000
        self.cart_value_surcharge_limit_cents = 1000
        self.number_of_items_surcharge_limit = 4
        self.number_of_items_surcharge_fee_cents = 50
        self.number_of_items_bulk_limit = 12
        self.number_of_items_bulk_fee_cents = 120
        self.delivery_distance_start_meters = 1000
        self.delivery_distance_start_fee_cents = 200
        self.delivery_distance_additional_length_meters = 500
        self.delivery_distance_additional_length_fee_cents = 100
        self.time_rush_weekday = 4 # Monday... Sunday = 0... 6
        self.time_rush_start_hour = time(hour = 15)
        self.time_rush_end_hour = time(hour = 19)
        self.time_rush_multiplier = 1.2
        self.max_delivery_fee = 1500

    def add_delivery_distance_fee(self, delivery_fee: int | float, delivery_distance: int) -> int | float:
        '''Adds fees related to delivery_distance to the delivery_fee.
        
        Adds a base fee for the set amount of starting meters of the delivery_distance.
        If the delivery is longer than that, for the beginning of each additional
        set length in the delivery_distance, a fee is added to delivery_fee.
        '''

        delivery_fee += self.delivery_distance_start_fee_cents
        if delivery_distance >= self.delivery_distance_start_meters:
            delivery_distance -= self.delivery_distance_start_meters
        else:
            delivery_distance = 0
        number_of_additional_distance_lengths = ceil(delivery_distance / self.delivery_distance_additional_length_meters)
        delivery_fee += number_of_additional_distance_lengths * self.delivery_distance_additional_length_fee_cents
        return delivery_fee

    def add_number_of_items_fee(self, delivery_fee: int | float, number_of_items: int) -> int | float:
        '''Adds fees related to the number_of_items to the delivery_fee.
        
        If the number_of_items is greater than the surcharge limit,
        a surcharge is added to the delivery_fee for each item above the limit. 
        If the number_of_items is greater than the bulk surcharge limit,
        a bulk fee is added to the delivery_fee.
        '''

        if number_of_items > self.number_of_items_surcharge_limit:
            number_of_surcharges = number_of_items - self.number_of_items_surcharge_limit
            delivery_fee += number_of_surcharges * self.number_of_items_surcharge_fee_cents
        if number_of_items > self.number_of_items_bulk_limit:
            delivery_fee += self.number_of_items_bulk_fee_cents
        return delivery_fee
    
    def add_cart_value_fee(self, delivery_fee: int | float, cart_value: int) -> int | float:
        '''Adds fees related to the cart_value to the delivery_fee.

        If cart_value is less than the surcharge limit,
        a surcharge equalling to the difference between 
        the surcharge limit and cart_value is added to the delivery_fee. 
        If the cart_value is equal to or more than the free delivery limit, 
        the delivery is free of charge. 
        '''

        if cart_value < self.cart_value_surcharge_limit_cents:
            delivery_fee += self.cart_value_surcharge_limit_cents - cart_value
        elif cart_value >= self.cart_value_free_delivery_limit_cents:
            delivery_fee = 0
        return delivery_fee

    def add_time_fee(self, delivery_fee: int | float, time: str) -> int | float:
        '''Adds fees related to time to the delivery_fee.

        If the ISO timestamp is within the set rush day and hours,
        the delivery_fee is multiplied with the set rush multiplier.
        '''

        time_as_datetime = parser.parse(time)
        day_of_the_week = datetime.weekday(time_as_datetime)
        if day_of_the_week == self.time_rush_weekday:
            if self.time_rush_start_hour <= time_as_datetime.time() <= self.time_rush_end_hour:
                delivery_fee *= self.time_rush_multiplier
        return delivery_fee
    
    def apply_max_delivery_fee(self, delivery_fee: int | float) -> int | float:
        '''Limits the delivery fee within the set maximum.'''

        if delivery_fee > self.max_delivery_fee:
            delivery_fee = self.max_delivery_fee
        return delivery_fee
    
    def post(self):
        '''Calculates delivery fee based on parameters in the request.

        Returns a JSON with the calculated delivery_fee.
        POST endpoint to URL /delivery-fee.
        '''

        request_data = request.get_json()
        try:
            # Validate the request data with marshmallow
            validated_request_data = delivery_fee_schema.load(data=request_data)
        except ValidationError as error:
            return {'message': 'Validation errors', 'errors': error.messages_dict}, HTTPStatus.BAD_REQUEST
        
        # dict key: function for calculating delivery fee
        # dict value: name of key in request whose value to use as argument
        delivery_fee_functions = {
            self.add_delivery_distance_fee: 'delivery_distance',
            self.add_number_of_items_fee: 'number_of_items',
            self.add_cart_value_fee: 'cart_value',
            self.add_time_fee: 'time',
            self.apply_max_delivery_fee: None
        }
        # calculate delivery fee
        delivery_fee = 0
        for function, key_name in delivery_fee_functions.items():
            if key_name is not None:
                delivery_fee = function(delivery_fee, validated_request_data[key_name])
            else:
                delivery_fee = function(delivery_fee)   
        return {'delivery_fee': int(delivery_fee)}, HTTPStatus.OK