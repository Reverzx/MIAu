import pytest
from loguru import logger
from api_actions.api_login import LoginAPI
from test_data.user_details import UserDetails
from test_data.user_creds import UserCredentials
from test_data.login_data import invalid_login_data_api


def test_successful_post_login():
    """
    Verifies that the response status code is 200 for a successful
    POST request to the /users/login endpoint.
    """
    login = LoginAPI()
    response = login.post_login(UserCredentials.it_email, UserCredentials.it_password)
    assert response.status_code == 200
    logger.success("Response status code is 200")


def test_post_login_response_schema():
    """
    Verifies that the JSON response from a successful POST request
    to the /users/login endpoint matches to the expected response schema.
    """
    login = LoginAPI()
    assert login.is_response_schema_correct(UserCredentials.it_email,
                                            UserCredentials.it_password)
    logger.success("JSON-response corresponds to the schema")


def test_post_login_response_text():
    """
    Verifies that the values returned in the response body after a successful
    POST request to the /users/login endpoint match the expected user details.
    """
    login = LoginAPI()
    response = login.post_login(UserCredentials.it_email,
                                UserCredentials.it_password)
    json_data = response.json()
    assert 'token' in json_data
    assert json_data['user']['_id'] == UserDetails.it_details['_id']
    assert json_data['user']['firstName'] == UserDetails.it_details['firstName']
    assert json_data['user']['lastName'] == UserDetails.it_details['lastName']
    assert json_data['user']['email'] == UserDetails.it_details['email']
    logger.success("Response body text contains correct user details")


@pytest.mark.parametrize('email, password, description', invalid_login_data_api)
def test_post_login_401(email, password, description):
    """
    Verifies that the response status code is 401 (Unauthorized) for a failed
    POST request to the /users/login endpoint using invalid credentials.
    """
    logger.info(f"Test: POST /users/login with {description}")
    login = LoginAPI()
    response = login.post_login(email, password)
    assert response.status_code == 401
    logger.success("Response status code is 401")


def test_post_login_missing_email_parameter():
    """
    Verifies that the response status code is 401 (Unauthorized)
    for a failed POST request to the /users/login endpoint
    when the request body is missing the email parameter.
    """
    login = LoginAPI()
    response = login.post_login_with_missing_email_parameter(UserCredentials.it_password)
    assert response.status_code == 401
    logger.success("Response status code is 401")


def test_post_login_missing_password_parameter():
    """
    Verifies that the response status code is 401 (Unauthorized)
    for a failed POST request to the /users/login endpoint
    when the request body is missing the password parameter.
    """
    login = LoginAPI()
    response = login.post_login_with_missing_password_parameter(UserCredentials.it_email)
    assert response.status_code == 401
    logger.success("Response status code is 401")
