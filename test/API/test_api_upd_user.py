import pytest
from loguru import logger
from api_actions.api_user_actions import UserActsApi
from api_actions.post_login import post_login
from test_data.users_schemas import (
    update_and_get_user_profile_response_schema,
    signin_and_login_user_response_schema
)
from test_data.usr_update_data import user_to_be_update, upd_data
from test_data.usr_update_data import (
    upd_usr_with_empty_fields,
    invalid_data_to_upd,
    upd_usr_with_some_empty_fields
)


def test_upd_user(revert_updation):
    """
    Verifies, that the responce status code is 200,
    Update User PATCH request is successful
    """
    update = UserActsApi()
    response = update.patch_upd_user(user_to_be_update, upd_data)
    assert response.status_code == 200, \
        f'Status code is {response.status_code}, expected 200'
    assert update.is_response_schema_correct(
        response,
        update_and_get_user_profile_response_schema
    ), \
        f'Response schema does not match, got {response.json()}'
    logger.success('User profile is successfully updated')


def test_login_after_update(revert_updation):
    """
    Verifies the login after updating user.
    Checks the status code and response body
    """
    update = UserActsApi()
    update.patch_upd_user(user_to_be_update, upd_data)
    response = post_login(upd_data["email"], upd_data["password"])
    assert response.status_code == 200, \
        f'Status code is {response.status_code}, expected 200'
    assert update.is_response_schema_correct(
        response,
        signin_and_login_user_response_schema
    ), f'Response schema does not match, got {response.json()}'
    logger.success('User with updated data successfully logged in')


@pytest.mark.parametrize('body, description, field_name', upd_usr_with_empty_fields)
def test_upd_user_with_empty_fields(body, description, field_name):
    """
    Verifies updating user with empty fields
    """
    logger.info(f'Update user with invalid credentials: {description}')
    update = UserActsApi()
    response = update.upd_usr_with_invalid_data(user_to_be_update, body)
    assert response.status_code == 400, \
        f'Status code is {response.status_code}, expected 400'
    logger.success(f'User updation flopped status code 400. {field_name} field is required.')


@pytest.mark.parametrize('body, description', invalid_data_to_upd)
def test_upd_user_with_invalid_data(body, description):
    """
    Verifies updating user vith invalid email and password
    """
    logger.info(f'Update user with invalid credentials: {description}')
    update = UserActsApi()
    response = update.upd_usr_with_invalid_data(user_to_be_update, body)
    assert response.status_code == 400, \
        f'Status code is {response.status_code}, expected 400'
    logger.success('User updation flopped status code 400.')


@pytest.mark.parametrize('body, description, field_name', upd_usr_with_some_empty_fields)
def test_get_profile_after_failed_update(body, description, field_name):
    """
    Verifies, that users data didn't change after flopped updating
    """
    logger.info(f'Update user with invalid credentials: {description}')
    update = UserActsApi()
    fail_upd = update.upd_usr_with_invalid_data(user_to_be_update, body)
    assert fail_upd.status_code == 400, \
        f'Status code is {fail_upd.status_code}, expected 400'
    response = update.get_user_profile(user_to_be_update)
    assert response.json()[field_name] == user_to_be_update[field_name], \
        f'Expected {user_to_be_update[field_name]} in {field_name}, '
    f'but {response.json()[field_name]} got'
    logger.success(f'User updation failed. {field_name} did not change.')
