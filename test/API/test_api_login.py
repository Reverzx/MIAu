import pytest
from loguru import logger
from api_actions.post_login import post_login
from test_data.user_creds import UserCredentials
from test_data.login_data import invalid_login_data_api
from api_actions.validate_response_schema import validate_response_schema


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.api
def test_successful_post_login(read_schema):
    # Run POST login
    response = post_login(UserCredentials.it_email,
                          UserCredentials.it_password)

    # Check the response status code
    assert response.status_code == 200, \
        f"Wrong status code: {response.status_code}. Expected: 200"
    logger.success("Response status code is 200")

    # Check the response schema
    actual_schema = response.json()
    expected_schema = read_schema["post_login"]
    validate_response_schema(actual_schema, expected_schema)


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize('email, password, description', invalid_login_data_api)
def test_post_login_fails_with_invalid_creds(email, password, description):
    logger.info(f"Test: POST /users/login with {description}")
    response = post_login(email, password)
    assert response.status_code == 401, \
        f"Wrong status code: {response.status_code}. Expected: 401"
    logger.success("Response status code is 401")


@pytest.mark.api
def test_post_login_missing_email_parameter():
    response = post_login("", UserCredentials.it_password)
    assert response.status_code == 401, \
        f"Wrong status code: {response.status_code}. Expected: 401"
    logger.success("Response status code is 401")


@pytest.mark.api
def test_post_login_missing_password_parameter():
    response = post_login(UserCredentials.it_email, "")
    assert response.status_code == 401, \
        f"Wrong status code: {response.status_code}. Expected: 401"
    logger.success("Response status code is 401")
