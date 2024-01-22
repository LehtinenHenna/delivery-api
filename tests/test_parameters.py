from http import HTTPStatus
free_delivery_limit = 200
cart_value_surcharge_limit = 1000
number_of_items_surcharge_limit_inclusive = 5
delivery_distance_start_meters = 1000
delivery_distance_start_fee = 200
delivery_distance_additional_meters = 500
delivery_distance_additional_fee = 100
# first element of each tuple: request_json parameter
# second element of each tuple: expected_response parameter
# third element of each tuple: expected_http_status
delivery_fee_post_parameters = [
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
            "message": "Invalid request"
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
            "message": "Invalid request"
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
            "number_of_items": 6, # 2 * 0.50€ = 1€ surcharge
            "time": "2024-01-15T13:00:00Z" # 0€ surcharge
        },
        {
            "delivery_fee": 300
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
    ( # test max delivery fee
        {
            "cart_value": 500, # 5€ surcharge
            "delivery_distance": 3000, # 2€ + 4€ = 6€
            "number_of_items": 13, # 9 * 0.50€ + 1.20€ = 5.70€ surcharge
            "time": "2024-01-19T15:10:00Z" # multiply fee by 1.2
        },
        {
            "delivery_fee": 1500 # 5€ + 6€ + 5.70€ = 16.70€. 16.70€ * 1.2 = 20.04. Max delivery fee 15€.
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
    ( # test with cart value hitting the free delivery limit
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