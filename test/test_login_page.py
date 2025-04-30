import pytest
from loguru import logger
from test_data.env import Env
from pages.login_page import LoginPage
from test_data.user_creds import UserCredentials


def test_login_with_valid_creds(driver):
    logger.info("Test: Authorization with valid credentials")
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.login_as(UserCredentials.it_email,
                              UserCredentials.it_password)
    assert login_page.is_login_successful()
    logger.success("Login succeeded for valid user")


@pytest.mark.parametrize('email, password, description', [
    ('240425test @test.com', UserCredentials.it_password, "Invalid email format (space)"),
    ('240425test@test.', UserCredentials.it_password, "Invalid email format (no domain)"),
    (UserCredentials.it_email, 'Passw0rd', "Wrong password"),
    (UserCredentials.not_registered_email, UserCredentials.it_password,
     "Email of a not registered user"),
    ('', UserCredentials.it_password, "Missing email"),
    (UserCredentials.it_email, '', "Missing password"),
    (UserCredentials.updated_old_email, UserCredentials.updated_old_password,
     "Old credentials after update"),
    (UserCredentials.deleted_email, UserCredentials.deleted_password,
     "Credentials of a deleted user"),
])
def test_login_with_invalid_creds(driver, email, password, description):
    logger.info(f"Test: Authorization with {description}")
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.login_as(email, password)
    assert login_page.is_login_page()
    assert login_page.is_error_present()
    assert login_page.is_error_text_correct()
    logger.success("Login failed as expected with error message.")


def test_login_with_recently_updated_creds(driver):
    logger.info("Test: Authorization with recently updated credentials")
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.login_as(UserCredentials.updated_new_email,
                              UserCredentials.updated_new_password)
    assert login_page.is_login_successful()
    logger.success("Login succeeded for valid user with recently updated credentials")
