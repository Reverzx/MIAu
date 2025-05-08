from loguru import logger
from pages.api_user_actions import UserActsApi
from test_data.register_data import usr_to_delete


def test_del_user():
    delete = UserActsApi()
    response = delete.delete_user(usr_to_delete)
    assert response.status_code == 200
    logger.success('Response status code is 200. User is deleted')
    delete.post_sign_up(usr_to_delete)


def test_verify_response_text():
    delete = UserActsApi()
    response = delete.delete_user(usr_to_delete)
    assert response.text == ''
    logger.success('Response contains to text')
    delete.post_sign_up(usr_to_delete)


def test_del_user_two_times():
    delete = UserActsApi()
    response = delete.double_delete_user(usr_to_delete)
    assert response.status_code == 401
    assert 'error' in response.json()
    assert response.json()['error'] == 'Please authenticate.'
    logger.success('Response status code is 401. Response contains expected text')
    delete.post_sign_up(usr_to_delete)


def test_get_deleted_user():
    delete = UserActsApi()
    response = delete.get_deleted_user(usr_to_delete)
    assert response.status_code == 401
    assert 'error' in response.json()
    assert response.json()['error'] == 'Please authenticate.'
    logger.success('Response status code is 401. Response contains expected text')
    delete.post_sign_up(usr_to_delete)
