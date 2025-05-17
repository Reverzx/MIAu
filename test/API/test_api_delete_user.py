from loguru import logger
from api_actions.api_user_actions import UserActsApi
from test_data.register_data import usr_to_delete


def test_del_user_status_code():
    """
    Verifies the response status code of User Delete
    """
    delete = UserActsApi()
    response = delete.delete_user(usr_to_delete)
    assert response.status_code == 200, \
        f'Status code is {response.status_code}, expected 200'
    logger.success('User is successfully deleted with response status code 200')
    delete.post_sign_up(usr_to_delete)


def test_verify_delete_user_response_text():
    """
    Verifies, that response text of Delete User is empty
    """
    delete = UserActsApi()
    response = delete.delete_user(usr_to_delete)
    assert response.text == '', \
        f'Got response text {response.text}'
    logger.success('Response contains no text as expected. User is successfully deleted')
    delete.post_sign_up(usr_to_delete)


def test_del_user_two_times():
    """
    Tries to delete the same user two times. Checks the response
    """
    delete = UserActsApi()
    response = delete.double_delete_user(usr_to_delete)
    assert response.status_code == 401, \
        f'Status code is {response.status_code}, expected 401'
    assert 'error' in response.json(), \
        f'Response JSON has no attribute "error", {response.json()}'
    assert response.json()['error'] == 'Please authenticate.'
    logger.success('Response status code is 401. Response contains expected error message')
    delete.post_sign_up(usr_to_delete)


def test_get_deleted_user():
    """
    Tries to get deletes user's profile. Checks the response
    """
    delete = UserActsApi()
    response = delete.get_deleted_user(usr_to_delete)
    assert response.status_code == 401, \
        f'Status code is {response.status_code}, expected 401'
    assert 'error' in response.json(), \
        f'Response JSON has no attribute "error", {response.json()}'
    assert response.json()['error'] == 'Please authenticate.'
    logger.success('Response status code is 401. Response contains expected error message')
    delete.post_sign_up(usr_to_delete)
