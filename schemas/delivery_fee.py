'''Schemas for data validation.

This module contains the class DeliveryFeeSchema 
for validating JSON data.
'''
from marshmallow import Schema, fields

class DeliveryFeeSchema(Schema):
    '''
    Validates JSON data with marshmallow.
    
    ...

    Attributes
    ----------
    cart_value: fields.Integer
        Validates that the field is given and that it's of type int.
    delivery_distance: fields.Integer
        Validates that the field is given and that it's of type int.
    number_of_items: fields.Integer
        Validates that the field is given and that it's of type int.
    time: fields.String
        Validates that the field is given and that it's of type str. 
    '''

    cart_value = fields.Integer(required=True)
    delivery_distance = fields.Integer(required=True)
    number_of_items = fields.Integer(required=True)
    time = fields.String(required=True)
