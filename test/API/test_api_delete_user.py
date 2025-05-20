import pytest
from loguru import logger
import requests
from api_actions.api_user_actions import UserActsApi
from test_data.register_data import usr_to_delete


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.api
def test_del_user(sign_up_user):
    """
    Verifies the response status code of User Delete
    """
    delete = UserActsApi()
    header = delete.get_header(usr_to_delete)
    response = delete.delete_user(header)
    assert response.status_code == 200, \
        f'Status code is {response.status_code}, expected 200'
    assert response.text == '', \
        f'Got response text {response.text}'
    logger.success('User is successfully deleted')


@pytest.mark.api
def test_del_user_two_times(sign_up_user):
    """
    Tries to delete the same user two times. Checks the response
    """
    delete = UserActsApi()
    header = delete.get_header(usr_to_delete)
    delete.delete_user(header)
    response = delete.delete_user(header)
    assert response.status_code == 401, \
        f'Status code is {response.status_code}, expected 401'
    assert 'error' in response.json(), \
        f'Response JSON has no attribute "error", {response.json()}'
    assert response.json()['error'] == 'Please authenticate.'
    logger.success('Response status code is 401. Response contains expected error message')


@pytest.mark.api
def test_get_deleted_user(sign_up_user):
    """
    Tries to get deletes user's profile. Checks the response
    """
    delete = UserActsApi()
    header = delete.get_header(usr_to_delete)
    delete.delete_user(header)
    response = requests.get(url=delete.usr_profile_url, headers=header)
    assert response.status_code == 401, \
        f'Status code is {response.status_code}, expected 401'
    assert 'error' in response.json(), \
        f'Response JSON has no attribute "error", {response.json()}'
    assert response.json()['error'] == 'Please authenticate.'
    logger.success('Response status code is 401. Response contains expected error message')
