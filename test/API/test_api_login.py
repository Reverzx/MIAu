import pytest
from loguru import logger
from test_data.user_details import UserDetails
from test_data.user_creds import UserCredentials
from test_data.login_data import invalid_login_data_api
from api_actions.validate_response_schema import validate_response_schema
from api_actions.post_login import post_login


def test_successful_post_login():
    """
    Verifies that the response status code is 200 for a successful
    POST request to the /users/login endpoint.
    """
    response = post_login(UserCredentials.it_email,
                          UserCredentials.it_password)
    assert response.status_code == 200
    logger.success("Response status code is 200")


def test_post_login_response_schema(read_schema):
    schema = read_schema["post_login"]
    response = post_login(UserCredentials.it_email,
                          UserCredentials.it_password)
    validate_response_schema(response, schema)
    logger.success("JSON-response corresponds to the schema")


def test_post_login_response_body():
    response = post_login(UserCredentials.it_email,
                          UserCredentials.it_password)
    json_data = response.json()
    assert 'token' in json_data
    assert json_data['user']['_id'] == UserDetails.it_details['_id']
    assert json_data['user']['firstName'] == UserDetails.it_details['firstName']
    assert json_data['user']['lastName'] == UserDetails.it_details['lastName']
    assert json_data['user']['email'] == UserDetails.it_details['email']
    logger.success("Response body text contains correct user details")


@pytest.mark.parametrize('email, password, description', invalid_login_data_api)
def test_post_login_fails_with_invalid_creds(email, password, description):
    logger.info(f"Test: POST /users/login with {description}")
    response = post_login(email, password)
    assert response.status_code == 401
    logger.success("Response status code is 401")


def test_post_login_missing_email_parameter():
    response = post_login("", UserCredentials.it_password)
    assert response.status_code == 401
    logger.success("Response status code is 401")


def test_post_login_missing_password_parameter():
    response = post_login(UserCredentials.it_email, "")
    assert response.status_code == 401
    logger.success("Response status code is 401")
