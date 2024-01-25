# Delivery API

This program is an API application for a delivery service.

# Installation

To install dependencies, run the following command in a terminal:

```
pip3 install -r requirements.txt
```

# Running the application
To start the server, run the following commandc:
```
python3 main.py
```

# End points

## Delivery fee POST end point

- HTTP verb: POST
- Description: Calculates a delivery fee based on the given input parameters
- URL: http://localhost:5000/delivery-fee

### Request

JSON containing delivery parameters

#### Example

```
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
```

#### Field details

| Field             | Type    | Description                                                       | Example value                        |
|-------------------|---------|-------------------------------------------------------------------|--------------------------------------|
| cart_value        | Integer | Value of the shopping cart in cents.                              | 790 (790 cents = 7.90€)              |
| delivery_distance | Integer | The distance between the store and customer’s location in meters. | 2235 (2235 meters = 2.235 km)        |
| number_of_items   | Integer | The number of items in the customer's shopping cart.              | 4 (customer has 4 items in the cart) |
| time              | String  | Order time in UTC in ISO format.                                  | 2024-01-15T13:00:00Z                 |

### Response

JSON containing calculated delivery fee

#### Example

```
{"delivery_fee": 710}
```

#### Field details

| Field        | Type    | Description             | Example value              |
|--------------|---------|-------------------------|----------------------------|
| delivery_fee | Integer | Calculated delivery fee | 1000 (1000 cents = 10.00€) |

### Rules for calculating a delivery fee

- If the cart value is less than 10€, a small order surcharge is added to the delivery price. The surcharge is the difference between the cart value and 10€. For example if the cart value is 8.90€, the surcharge will be 1.10€.
- A delivery fee for the first 1000 meters (=1km) is 2€. If the delivery distance is longer than that, 1€ is added for every additional 500 meters that the courier needs to travel before reaching the destination. Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.
    - Example 1: If the delivery distance is 1499 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
    - Example 2: If the delivery distance is 1500 meters, the delivery fee is: 2€ base fee + 1€ for the additional 500 m => 3€
    - Example 3: If the delivery distance is 1501 meters, the delivery fee is: 2€ base fee + 1€ for the first 500 m + 1€ for the second 500 m => 4€
- If the number of items is five or more, an additional 50 cent surcharge is added for each item above and including the fifth item. An extra "bulk" fee applies for more than 12 items of 1,20€
    - Example 1: If the number of items is 4, no extra surcharge
    - Example 2: If the number of items is 5, 50 cents surcharge is added
    - Example 3: If the number of items is 10, 3€ surcharge (6 x 50 cents) is added
    - Example 4: If the number of items is 13, 5,70€ surcharge is added ((9 * 50 cents) + 1,20€)
- The delivery fee can never be more than 15€, including possible surcharges.
- The delivery is free (0€) when the cart value is equal or more than 200€.
- During the Friday rush, 3 - 7 PM, the delivery fee (the total fee including possible surcharges) will be multiplied by 1.2x. However, the fee still cannot be more than the max (15€). Considering timezone, for simplicity, use UTC as a timezone in backend solutions (so Friday rush is 3 - 7 PM UTC). In frontend solutions, use the timezone of the browser (so Friday rush is 3 - 7 PM in the timezone of the browser).


# Testing

To start the automated tests, run the following command while in the root folder (delivery-api) of the project:
```
python3 -m pytest tests
```
To send a post request manually while the Flask server is running, you can use the curl command with the --json option. For example:
```
curl --json '{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}'  http://localhost:5000/delivery-fee
```

# Development

## Updating requirements.txt

Install pipreqs if you don't have it in your system:
```
pip3 install pipreqs
```
Then run the following command to update requirements.txt:
```
pipreqs --force
```