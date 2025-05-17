import pytest
from loguru import logger
from api_actions.api_user_actions import UserActsApi
from test_data.register_data import usr_to_add, exist_usr, invalid_reg_data_api
from test_data.users_schemas import (
    signin_and_login_user_response_schema,
    update_and_get_user_profile_response_schema)


def test_post_sign_up_status_code(delete_user):
    """
    Verifies, that the responce status code is 201,
    SignUp POST request is successful
    """
    register = UserActsApi()
    response = register.post_sign_up(usr_to_add)
    assert response.status_code == 201, \
        f'Status code is {response.status_code}, expected 201'
    logger.success("Response status code is 201")


def test_signup_response_schema(delete_user):
    """
    Verifies, that response schema mathes vith expected schema
    """
    register = UserActsApi()
    response = register.post_sign_up(usr_to_add)
    assert register.is_response_schema_correct(
        response,
        signin_and_login_user_response_schema), \
        f'Response schema does not match, got {response.json()}'
    logger.success('Got response json matches with expected schema')


def test_get_profile_after_registration(delete_user):
    """
    Verifies, that user profile filled correctly
    """
    register = UserActsApi()
    register.post_sign_up(usr_to_add)
    response = register.get_user_profile(usr_to_add)
    assert response.status_code == 200, \
        f'Status code is {response.status_code}, expected 200'
    assert register.is_response_schema_correct(
        response,
        update_and_get_user_profile_response_schema), \
        f'Response schema does not match, got {response.json()}'
    assert response.json()['email'] == usr_to_add['email'], \
        'Got email does not match with expected'
    logger.success('User was successfully registered')


def test_add_exist_user():
    """
    Verifies that trying to register user, which is already registered, flops.
    """
    register = UserActsApi()
    response = register.sign_up_with_invalid_data(exist_usr)
    assert response.status_code == 400, \
        f'Status code is {response.status_code}, expected 400'
    assert 'Email address is already in use' in response.json()['message']
    logger.success("Registrtion is failed, user has already been registered")


@pytest.mark.parametrize('body, description', invalid_reg_data_api)
def test_register_user_with_invalid_data(body, description):
    """
    Verifies registration a new user with incorrect credentials.
    """
    logger.info(f'Registration user with invalid creds {description}')
    register = UserActsApi()
    response = register.sign_up_with_invalid_data(body)
    assert response.status_code == 400, \
        f'Status code is {response.status_code}, expected 400'
    logger.success("Registration with invalid data flopped with response status code is 400")
