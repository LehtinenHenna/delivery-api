'''Schemas for data validation.

This module contains the class DeliveryFeeSchema 
for validating JSON data.
'''
from datetime import timezone, datetime
from marshmallow import Schema, fields, validate, validates, ValidationError

class DeliveryFeeSchema(Schema):
    '''
    Validates JSON data with marshmallow.
    
    ...

    Attributes
    ----------
    cart_value: fields.Integer
        Validates that the field is given, and that it's of type int,
        and that the number is greater than zero.
    delivery_distance: fields.Integer
        Validates that the field is given, and that it's of type int,
        and that the number is greater than zero.
    number_of_items: fields.Integer
        Validates that the field is given, and that it's of type int,
        and that the number is greater than zero.
    time: fields.AwareDateTime
        Validates that the field is given, and that it's of type datetime.
    
    Methods
    -------
    validates_time(time_as_datetime: datetime)
        Provides extra validation for time to make sure it's in UTC time zone.
    '''

    cart_value = fields.Integer(required=True, validate=[
        validate.Range(min=1, error="Value must be greater than 0.")])
    delivery_distance = fields.Integer(required=True, validate=[
        validate.Range(min=1, error="Value must be greater than 0.")])
    number_of_items = fields.Integer(required=True, validate=[
        validate.Range(min=1, error="Value must be greater than 0.")])
    time = fields.AwareDateTime(required=True)

    @validates("time")
    def validates_time(self, time_as_datetime: datetime) -> datetime:
        '''Validates that time is in UTZ timezone.'''
        if time_as_datetime.tzinfo != timezone.utc:
            raise ValidationError('Not a valid datetime.')
        return time_as_datetime
