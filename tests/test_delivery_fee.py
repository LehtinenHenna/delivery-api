import pytest
from main import DeliveryApi
from test_parameters import delivery_fee_post_parameters


@pytest.mark.parametrize(
    "request_json, expected_response, expected_http_status", delivery_fee_post_parameters
)
def test_delivery_fee_post(request_json, expected_response, expected_http_status):
    delivery_api = DeliveryApi()
    with delivery_api.app.test_client() as client:
        response = client.post('/delivery-fee', json=request_json)
        assert response.status_code == expected_http_status
        assert response.data == expected_response