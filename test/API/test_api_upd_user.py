import pytest
from loguru import logger
from pages.api_user_actions import UserActsApi
from pages.api_login import LoginAPI
from test_data.usr_update_data import usr_to_be_update, upd_data
from test_data.usr_update_data import upd_usr_with_empty_fields as ef, invalid_data_to_upd as invd


def test_upd_user_200():
    """
    Verifies, that the responce status code is 200,
    Update User PATCH request is successful
    """
    update = UserActsApi()
    response = update.patch_upd_user(usr_to_be_update, upd_data)
    assert response.status_code == 200
    logger.success('Response status code is 201')
    update.patch_upd_user(upd_data, usr_to_be_update)


def test_response_upd_body():
    """
    Verifies, that response body contains the necessary data
    """
    update = UserActsApi()
    response = update.patch_upd_user(usr_to_be_update, upd_data)
    data_to_check = response.json()
    assert '_id' in data_to_check
    assert '__v' in data_to_check
    assert data_to_check['firstName'] == upd_data['firstName']
    assert data_to_check['lastName'] == upd_data['lastName']
    assert data_to_check['email'] == upd_data['email']
    logger.success('Response body contains all the necessary details')
    update.patch_upd_user(upd_data, usr_to_be_update)


def test_update_user_response_schema():
    """
    Verifies that response JSON mathes to the expected recponse schema
    """
    update = UserActsApi()
    assert update.is_response_update_schema_correct(usr_to_be_update, upd_data)
    logger.success("Correct response JSON schema")
    update.patch_upd_user(upd_data, usr_to_be_update)


def test_login_after_update():
    """
    Verifies the login after updating user.
    Checks the status code and response body
    """
    update = UserActsApi()
    update.patch_upd_user(usr_to_be_update, upd_data)
    login = LoginAPI()
    response = login.post_login(upd_data['email'], upd_data['password'])
    assert response.status_code == 200
    logger.success('Response status code is 200')
    data_to_check = response.json()
    assert 'token' in data_to_check
    assert '_id' in data_to_check['user']
    assert data_to_check['user']['firstName'] == upd_data['firstName']
    assert data_to_check['user']['lastName'] == upd_data['lastName']
    assert data_to_check['user']['email'] == upd_data['email']
    logger.success('Response body contains all the necessary details')
    update.patch_upd_user(upd_data, usr_to_be_update)


def test_get_updated_user():
    """
    Verifies getting updated user's profile data.
    Checks, that got data mathes with sent data.
    """
    update = UserActsApi()
    update.patch_upd_user(usr_to_be_update, upd_data)
    response = update.get_user_profile(upd_data)
    data_to_check = response.json()
    assert '_id' in data_to_check
    assert '__v' in data_to_check
    assert data_to_check['firstName'] == upd_data['firstName']
    assert data_to_check['lastName'] == upd_data['lastName']
    assert data_to_check['email'] == upd_data['email']
    logger.success('Response body contains all the necessary details')
    update.patch_upd_user(upd_data, usr_to_be_update)


@pytest.mark.parametrize('body, description, field_name', ef)
def test_upd_user_with_empty_fields(body, description, field_name):
    """
    Verifies updating user with empty fields
    """
    logger.info(f'Update user with invalid credentials: {description}')
    update = UserActsApi()
    response = update.upd_usr_with_invalid_data(usr_to_be_update, body)
    assert response.status_code == 400
    logger.success(f'Response status code is 400. {field_name} field is required.')


@pytest.mark.parametrize('body, description', invd)
def test_upd_user_with_invalid_data(body, description):
    """
    Verifies updating user vith invalid email and password
    """
    logger.info(f'Update user with invalid credentials: {description}')
    update = UserActsApi()
    response = update.upd_usr_with_invalid_data(usr_to_be_update, body)
    assert response.status_code == 400
    logger.success(f'Response status code is 400.')


@pytest.mark.parametrize('body, description, field_name', ef)
def test_get_profile_after_failed_update(body, description, field_name):
    """
    Verifies, that users data didn't change after flopped updating
    """
    logger.info(f'Update user with invalid credentials: {description}')
    update = UserActsApi()
    update.upd_usr_with_invalid_data(usr_to_be_update, body)
    response = update.get_user_profile(usr_to_be_update)
    assert response.status_code == 200
    data_to_check = response.json()
    assert '_id' in data_to_check
    assert '__v' in data_to_check
    assert data_to_check['firstName'] == usr_to_be_update['firstName']
    assert data_to_check['lastName'] == usr_to_be_update['lastName']
    assert data_to_check['email'] == usr_to_be_update['email']
    logger.success(f'Response status code is 200. {field_name} did not change.')
