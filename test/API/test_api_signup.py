import pytest
from loguru import logger
from api_actions.api_user_actions import UserActsApi
from api_actions.validate_response_schema import validate_response_schema
from test_data.register_data import user_to_add, exist_user, invalid_reg_data_api
from test_data.users_schemas import (
    signin_and_login_user_response_schema,
    update_and_get_user_profile_response_schema)


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.api
def test_post_sign_up(delete_user):
    """
    Verifies, that the responce status code is 201,
    SignUp POST request is successful
    """
    register = UserActsApi()
    response = register.post_sign_up(user_to_add)
    assert response.status_code == 201, \
        f'Status code is {response.status_code}, expected 201'
    assert validate_response_schema(
        signin_and_login_user_response_schema,
        response.json()
    ), f'Response schema does not match, got {response.json()}'
    logger.success("New user is successfully registered")


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.api
def test_get_new_profile(delete_user):
    """
    Verifies, that user profile filled correctly
    """
    register = UserActsApi()
    register.post_sign_up(user_to_add)
    response = register.get_user_profile(user_to_add)
    assert response.status_code == 200, \
        f'Status code is {response.status_code}, expected 200'
    assert validate_response_schema(
        update_and_get_user_profile_response_schema,
        response.json()
    ), f'Response schema does not match, got {response.json()}'
    assert response.json()['email'] == user_to_add['email'], \
        'Got email does not match with expected'
    logger.success('User was successfully registered')


@pytest.mark.regression
@pytest.mark.api
def test_add_exist_user():
    """
    Verifies that trying to register user, which is already registered, flops.
    """
    register = UserActsApi()
    response = register.post_sign_up(exist_user)
    assert response.status_code == 400, \
        f'Status code is {response.status_code}, expected 400'
    assert 'Email address is already in use' in response.json()['message']
    logger.success("Registrtion is failed, user has already been registered")


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize('body, description', invalid_reg_data_api)
def test_register_user_with_invalid_data(body, description):
    """
    Verifies registration a new user with incorrect data.
    """
    logger.info(f'Registration user with invalid creds {description}')
    register = UserActsApi()
    response = register.post_sign_up(body)
    assert response.status_code == 400, \
        f'Status code is {response.status_code}, expected 400'
    logger.success("Registration with invalid data flopped with response status code is 400")
