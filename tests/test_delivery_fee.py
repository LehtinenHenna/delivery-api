'''Unit tests for the API.

Contains unit test cases that test the functionality of the delivery api.
pytest.mark.parametrize is utilized to run the same test multiple times
with different parameters. The parameters can be found in file parameters.py.
'''
from json import loads
import pytest
from parameters import delivery_fee_post_test_parameters
from main import DeliveryApi


@pytest.mark.parametrize(
    "request_json, expected_response, expected_http_status", delivery_fee_post_test_parameters
)
def test_delivery_fee_post(request_json: dict, expected_response: dict, expected_http_status: int):
    '''Tests the POST endpoint at URL /delivery-fee with multiple test cases.'''
    delivery_api = DeliveryApi()
    with delivery_api.app.test_client() as client:
        response = client.post('/delivery-fee', json=request_json)
        assert response.status_code == expected_http_status
        assert loads(response.data) == expected_response