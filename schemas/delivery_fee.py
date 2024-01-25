from marshmallow import Schema, fields

class DeliveryFeeSchema(Schema):
    cart_value = fields.Integer(required=True)
    delivery_distance = fields.Integer(required=True)
    number_of_items = fields.Integer(required=True)
    time = fields.String(required=True)
