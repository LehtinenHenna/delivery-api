''' This module contains parameters used for unit tests that utilize pytest.mark.parametrize.
'''
from http import HTTPStatus

delivery_fee_post_test_parameters = [
    # first element of each tuple: request_json parameter
    # second element of each tuple: expected_response parameter
    # third element of each tuple: expected_http_status parameter

    ( # test cart_value surcharge
        {
            "cart_value": 790, # 10€ - 7.9€ = 2.1€ surcharge
            "delivery_distance": 2235, # 2€ + 3€ = 5€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 710
        },
        HTTPStatus.OK
    ),
    ( # test empty request
        {},
        {
            'message': 'Validation errors', 
            'errors': {
                'cart_value': ['Missing data for required field.'], 
                'delivery_distance': ['Missing data for required field.'], 
                'number_of_items': ['Missing data for required field.'], 
                'time': ['Missing data for required field.']
            }
        },
        HTTPStatus.BAD_REQUEST
    ),
    ( # test request containing a wrong datatype
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": "invalid datatype",
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            'message': 'Validation errors', 'errors': {
                'delivery_distance': ['Not a valid integer.']
            }
        },
        HTTPStatus.BAD_REQUEST
    ),
    ( # test request containing negative numbers
        {
            "cart_value": -1, # negative number not allowed
            "delivery_distance": -1000, # negative number not allowed
            "number_of_items": -4, # negative number not allowed
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            'message': 'Validation errors', 'errors': {
                'cart_value': ['Value must be greater than 0.'],
                'delivery_distance': ['Value must be greater than 0.'], 
                'number_of_items': ['Value must be greater than 0.']
            }
        },
        HTTPStatus.BAD_REQUEST
    ),
    ( # test request containing zeroes
        {
            "cart_value": 0, # zero not allowed
            "delivery_distance": 0, # zero not allowed
            "number_of_items": 0, # zero not allowed
            "time": "2024-01-19T15:10:00Z" # multiply fee by 1.2
        },
        {
            'message': 'Validation errors', 'errors': {
                'cart_value': ['Value must be greater than 0.'],
                'delivery_distance': ['Value must be greater than 0.'], 
                'number_of_items': ['Value must be greater than 0.']
            }
        },
        HTTPStatus.BAD_REQUEST
    ),
    ( # test rounding delivery fee
        {
            "cart_value": 1, # 10€ - 0.01€ = 9.99€ surcharge
            "delivery_distance": 1, # 2€
            "number_of_items": 1, # 0€ surcharge
            "time": "2024-01-19T15:10:00Z" # multiply fee by 1.2: 1199c * 1.2 = 1438,8c
        },
        {
            "delivery_fee": 1439
        },
        HTTPStatus.OK
    ),
    ( # test time missing some of the timestamp data
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-15" # Invalid data
        },
        {
            'message': 'Validation errors', 'errors': {
                'time': ['Not a valid datetime.']
            }
        },
        HTTPStatus.BAD_REQUEST
    ),
    ( # test time missing timezone
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-15T13:00:00" # invalid data
        },
        {
            'message': 'Validation errors', 'errors': {
                'time': ['Not a valid aware datetime.']
            }
        },
        HTTPStatus.BAD_REQUEST
    ),
    ( # test time not being a valid ISO timestamp
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 4, # 0€ surcharge
            "time": "not valid time" # Invalid data
        },
        {
            'message': 'Validation errors', 'errors': {
                'time': ['Not a valid datetime.']
            }
        },
        HTTPStatus.BAD_REQUEST
    ),
    ( # test time of wrong timezone
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-06T19:20:34+02:00" # Invalid timezone
        },
        {
            'message': 'Validation errors', 'errors': {
                'time': ['Not a valid datetime.']
            }
        },
        HTTPStatus.BAD_REQUEST
    ),
    ( # test delivery distance of less than 1000
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 230, # 2€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 200
        },
        HTTPStatus.OK
    ),
    ( # test delivery distance of just under 1500
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1499, # 2€ + 1€ = 3€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 300
        },
        HTTPStatus.OK
    ),
    ( # test delivery distance of exactly 1500
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1500, # 2€ + 1€ = 3€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 300
        },
        HTTPStatus.OK
    ),
    ( # test delivery distance of just over 1500
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1501, # 2€ + 2€ = 4€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 400
        },
        HTTPStatus.OK
    ),
    ( # test number_of_items surcharge
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 5, # 1 * 0.50€ = 0.50€ surcharge
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 250
        },
        HTTPStatus.OK
    ),
    ( # test number_of_items surcharge
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 8, # 4 * 0.50€ = 2€ surcharge
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 400
        },
        HTTPStatus.OK
    ),
    ( # test number_of_items surcharge without bulk fee
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 12, # 8 * 0.50€ = 4€ surcharge
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 600
        },
        HTTPStatus.OK
    ),
    ( # test number_of_items surcharge with bulk fee
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 13, # 9 * 0.50€ + 1.20€ = 5.70€ surcharge
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 770
        },
        HTTPStatus.OK
    ),
    ( # test Friday rush
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-19T15:10:00Z" # multiply fee by 1.2
        },
        {
            "delivery_fee": 240
        },
        HTTPStatus.OK
    ),
    ( # test Friday rush start
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-19T15:00:00Z" # multiply fee by 1.2
        },
        {
            "delivery_fee": 240
        },
        HTTPStatus.OK
    ),
    ( # test Friday rush end
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-19T19:00:00Z" # multiply fee by 1.2
        },
        {
            "delivery_fee": 240
        },
        HTTPStatus.OK
    ),
    ( # test time just before Friday rush
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-19T14:59:59Z" # 0€ surcharge
        },
        {
            "delivery_fee": 200
        },
        HTTPStatus.OK
    ),
    ( # test time just after Friday rush
        {
            "cart_value": 1000, # 0€ surcharge
            "delivery_distance": 1000, # 2€
            "number_of_items": 4, # 0€ surcharge
            "time": "2024-01-19T19:01:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 200
        },
        HTTPStatus.OK
    ),
    ( # test max delivery fee
        {
            "cart_value": 500, # 5€ surcharge
            "delivery_distance": 3000, # 2€ + 4€ = 6€
            "number_of_items": 13, # 9 * 0.50€ + 1.20€ = 5.70€ surcharge
            "time": "2024-01-19T15:10:00Z" # multiply fee by 1.2
        },
        { # 5€ + 6€ + 5.70€ = 16.70€. 16.70€ * 1.2 = 20.04. Max delivery fee 15€.
            "delivery_fee": 1500 
        },
        HTTPStatus.OK
    ),
    ( # test with cart value just under the free delivery limit
        {
            "cart_value": 19999, # 0€ surcharge
            "delivery_distance": 3000, # 2€ + 4€ = 6€
            "number_of_items": 13, # 9 * 0.50€ + 1.20€ = 5.70€ surcharge
            "time": "2024-01-19T15:10:00Z" # multiply fee by 1.2
        },
        {
            "delivery_fee": 1404 # 6€ + 5.7€ = 11.70€. 11.70€ * 1.2 = 14.04€
        },
        HTTPStatus.OK
    ),
    ( # test with cart value hitting the free delivery limit without Friday rush
        {
            "cart_value": 20000, # 0€ surcharge
            "delivery_distance": 3000, # 2€ + 4€ = 6€
            "number_of_items": 13, # 9 * 0.50€ + 1.20€ = 5.70€ surcharge
            "time": "2024-01-20T15:10:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 0 # cart >= 200€, delivery free of charge
        },
        HTTPStatus.OK
    ),
    ( # test with cart value hitting the free delivery limit with Friday rush
        {
            "cart_value": 20000, # 0€ surcharge
            "delivery_distance": 3000, # 2€ + 4€ = 6€
            "number_of_items": 13, # 9 * 0.50€ + 1.20€ = 5.70€ surcharge
            "time": "2024-01-19T15:10:00Z" # multiply fee by 1.2
        },
        {
            "delivery_fee": 0 # cart >= 200€, delivery free of charge
        },
        HTTPStatus.OK
    ),
]
