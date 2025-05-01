import pytest
from loguru import logger
from test_data.env import Env
from pages.login_page import LoginPage
from test_data.user_creds import UserCredentials
from test_data.login_data import invalid_login_data_ui


def test_login_with_valid_creds(driver):
    """
    Verifies successful login with valid (registered) user credentials.
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.login_as(UserCredentials.it_email, UserCredentials.it_password)
    assert login_page.is_login_successful()
    logger.success("Login succeeded for valid user")


@pytest.mark.parametrize('email, password, description', invalid_login_data_ui)
def test_login_with_invalid_creds(driver, email, password, description):
    """
    Verifies that login fails and an appropriate error message is displayed
    when using invalid user credentials. Ensure that no redirect occurs.
    """
    logger.info(f"Test: Authorization with {description}")
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.login_as(email, password)
    assert login_page.is_login_page()
    assert login_page.is_error_present()
    assert login_page.is_error_text_correct()
    logger.success("Login failed as expected with error message.")


def test_login_with_recently_updated_creds(driver):
    """
    Verifies that a user can successfully log in with recently updated credentials.
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.login_as(UserCredentials.updated_new_email, UserCredentials.updated_new_password)
    assert login_page.is_login_successful()
    logger.success("Login succeeded for valid user with recently updated credentials")
