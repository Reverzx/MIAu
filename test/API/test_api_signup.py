import pytest
from loguru import logger
from pages.api_user_actions import UserActsApi
from test_data.register_data import usr_to_add, exist_usr, invalid_reg_data_api


def test_post_sign_up():
    """
    Verifies, that the responce status code is 201,
    SignUp POST request is successful
    """
    register = UserActsApi()
    response = register.post_sign_up(usr_to_add)
    assert response.status_code == 201
    logger.success("Response status code is 201")
    register.delete_user(usr_to_add)


def test_response_signup_body():
    """
    Verifies that response body contains all the expected data
    """
    register = UserActsApi()
    response = register.post_sign_up(usr_to_add)
    data_to_check = response.json()
    assert 'token' in data_to_check
    assert '_id' in data_to_check['user']
    assert data_to_check['user']['firstName'] == usr_to_add['firstName']
    assert data_to_check['user']['lastName'] == usr_to_add['lastName']
    assert data_to_check['user']['email'] == usr_to_add['email']
    logger.success('Response body contains all the necessary details')
    register.delete_user(usr_to_add)


def test_get_profile():
    """
    Verifies, that user profile filled correctly
    """
    register = UserActsApi()
    register.post_sign_up(usr_to_add)
    response = register.get_user_profile(usr_to_add)
    data_to_check = response.json()
    assert response.status_code == 200
    assert '_id' in data_to_check
    assert '__v' in data_to_check
    assert data_to_check['firstName'] == usr_to_add['firstName']
    assert data_to_check['lastName'] == usr_to_add['lastName']
    assert data_to_check['email'] == usr_to_add['email']
    logger.success('Response body contains all the necessary details')
    register.delete_user(usr_to_add)


def test_signup_response_schema():
    """
    Verifies that response JSON mathes to the expected recponse schema
    """
    register = UserActsApi()
    assert register.is_response_schema_correct(usr_to_add)
    logger.success("Correct response JSON schema")
    register.delete_user(usr_to_add)


def test_add_exist_user():
    """
    Verifies that trying to register user, which is already registered, flops.
    Status code 400
    """
    register = UserActsApi()
    response = register.sign_up_with_invalid_data(exist_usr)
    assert response.status_code == 400
    logger.success("Response status code is 400")


@pytest.mark.parametrize('body, description', invalid_reg_data_api)
def test_register_user_with_invalid_data(body, description):
    """
    Verifies registration a new user with incorrect credentials.
    Status code is 400
    """
    logger.info(f'Registration user with invalid creds {description}')
    register = UserActsApi()
    response = register.sign_up_with_invalid_data(body)
    assert response.status_code == 400
    logger.success("Response status code is 400")
