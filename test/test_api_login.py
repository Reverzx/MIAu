import pytest
from loguru import logger
from pages.api_login import LoginAPI
from test_data.user_details import UserDetails
from test_data.user_creds import UserCredentials


def test_post_login_200():
    logger.info("Test: Response status code for successful POST Log In")
    login = LoginAPI()
    response = login.post_login(UserCredentials.it_email,
                                UserCredentials.it_password)
    assert response.status_code == 200
    logger.success("Response status code is 200")


def test_post_login_response_schema():
    logger.info("Test: Response schema for successful POST Log In")
    login = LoginAPI()
    assert login.is_response_schema_correct(UserCredentials.it_email,
                                UserCredentials.it_password)
    logger.success("JSON-response corresponds to the schema")


def test_post_login_response_text():
    logger.info("Test: Response body text for successful POST Log In")
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


@pytest.mark.parametrize('email, password, description', [
    ('240425test @test.com', UserCredentials.it_password, "Invalid email format (space)"),
    ('240425test@test.', UserCredentials.it_password, "Invalid email format (no domain)"),
    (UserCredentials.it_email, 'Passw0rd', "Wrong password"),
    (UserCredentials.not_registered_email, UserCredentials.it_password,
     "Email of a not registered user"),
    (UserCredentials.updated_old_email, UserCredentials.updated_old_password,
     "Old credentials after update"),
    (UserCredentials.deleted_email, UserCredentials.deleted_password,
     "Credentials of a deleted user"),
    ("", UserCredentials.it_password, "Missing email"),
    (" ", UserCredentials.it_password, "Space as an email"),
    (None, UserCredentials.it_password, "None as an email"),
    (UserCredentials.it_email, "", "Missing password"),
    (UserCredentials.it_email, " ", "Space as an password"),
    (UserCredentials.it_email, None, "None as an password"),
])
def test_post_login_401(email, password, description):
    logger.info(f"Test: POST Log In with {description}")
    login = LoginAPI()
    response = login.post_login(email, password)
    assert response.status_code == 401
    logger.success("Response status code is 401")


def test_post_login_missing_email_parameter():
    logger.info("Test: POST Log In without email parameter in the request body")
    login = LoginAPI()
    response = login.post_login_with_missing_email_parameter(UserCredentials.it_password)
    assert response.status_code == 401
    logger.success("Response status code is 401")


def test_post_login_missing_password_parameter():
    logger.info("Test: POST Log In without password parameter in the request body")
    login = LoginAPI()
    response = login.post_login_with_missing_password_parameter(UserCredentials.it_email)
    assert response.status_code == 401
    logger.success("Response status code is 401")


def test_post_login_upd_creds_200():
    logger.info("Test: POST Log In with recently updated email/password")
    login = LoginAPI()
    response = login.post_login(UserCredentials.updated_new_email,
                                UserCredentials.updated_new_password)
    assert response.status_code == 200
    logger.success("Response status code is 200")
