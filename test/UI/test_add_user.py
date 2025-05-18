import pytest
from loguru import logger
from test_data.env import Env
from pages.login_page import LoginPage
from test_data.user_creds import UserCredentials as UC
from test_data.register_data import invalid_email_ui_data, short_pasword_ui_data


def test_add_user_with_valid_credentials(driver, delete_user):
    """
    Verifies successful registration vith valid user credentials
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    add_user_page = login_page.click_signup()
    assert add_user_page.is_add_user_page()
    add_user_page.fill_the_registration_form(UC.register_new_first_name,
                                            UC.register_new_last_name,
                                            UC.register_new_email,
                                            UC.register_new_password)
    add_user_page.submit()
    assert add_user_page.is_signup_successful()
    logger.success("New user is successfully added")


def test_sign_up_user_which_already_exists(driver):
    """
    Verifies, that registration flops if user is already registered
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    add_user_page = login_page.click_signup()
    assert add_user_page.is_add_user_page()
    add_user_page.fill_the_registration_form(UC.exist_usr_fname,
                                            UC.exist_usr_lname,
                                            UC.exist_usr_email,
                                            UC.exist_usr_password)
    add_user_page.submit()
    assert add_user_page.is_error_text_correct(add_user_page.err_registered_msg)
    logger.success("Registration failed as expected with error message")


def test_cancel_registration(driver):
    """
    Verifies returning to Login page after cancelling of Sign Up
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    add_user_page = login_page.click_signup()
    assert add_user_page.is_add_user_page()
    add_user_page.fill_the_registration_form(UC.register_new_first_name,
                                            UC.register_new_last_name,
                                            UC.register_new_email,
                                            UC.register_new_password)
    add_user_page.cancel()
    assert add_user_page.is_url_correct(f'{Env.URL_Login}login')
    logger.success('Registration is successfully canceled')


def test_add_user_without_first_name(driver):
    """
    Verifies, that registration flops if [First Name] field is not filled
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    add_user_page = login_page.click_signup()
    assert add_user_page.is_add_user_page()
    add_user_page.fill_the_registration_form(' ',
                                            UC.register_new_last_name,
                                            UC.register_new_email,
                                            UC.register_new_password)
    add_user_page.submit()
    assert add_user_page.is_error_text_correct(add_user_page.err_fname_msg)
    logger.success("Registration failed as expected with error message")


def test_add_user_without_last_name(driver):
    """
    Verifies, that registration flops if [Last Name] field is not filled
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    add_user_page = login_page.click_signup()
    assert add_user_page.is_add_user_page()
    add_user_page.fill_the_registration_form(UC.register_new_first_name,
                                            ' ',
                                            UC.register_new_email,
                                            UC.register_new_password)
    add_user_page.submit()
    assert add_user_page.is_error_text_correct(add_user_page.err_lname_msg)
    logger.success("Registration failed as expected with error message")


@pytest.mark.parametrize('first_name, last_name, email, password, description', invalid_email_ui_data)
def test_add_user_with_invalid_email(driver, first_name, last_name, email, password, description):
    """
    Verifies, that registration flops if [Email] is empty or filled with incorrect data
    """
    logger.info(f'Test: registration with {description}')
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    add_user_page = login_page.click_signup()
    assert add_user_page.is_add_user_page()
    add_user_page.fill_the_registration_form(first_name, last_name, email, password)
    add_user_page.submit()
    assert add_user_page.is_error_text_correct(add_user_page.err_email_msg)
    logger.success("Registration failed as expected with error message")


def test_add_user_without_password(driver):
    """
    Verifies, that registration flops if [Password] field is not filled
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    add_user_page = login_page.click_signup()
    assert add_user_page.is_add_user_page()
    add_user_page.fill_the_registration_form(UC.register_new_first_name,
                                            UC.register_new_password,
                                            UC.register_new_email,
                                            ' ')
    add_user_page.submit()
    assert add_user_page.is_error_text_correct(add_user_page.err_password_msg)
    logger.success("Registration failed as expected with error message")


@pytest.mark.parametrize('first_name, last_name, email, password',
                         short_pasword_ui_data)
def test_add_user_with_short_password(driver, first_name, last_name, email, password):
    """
    Verifies, that registration flops if password contains less than 7 symbols
    """
    logger.info(f'Test: registration with password {password}')
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    add_user_page = login_page.click_signup()
    assert add_user_page.is_add_user_page()
    add_user_page.fill_the_registration_form(first_name, last_name, email, password)
    add_user_page.submit()
    assert add_user_page.is_error_text_correct(
        f"User validation failed: password: Path `password` (`{password}`) "
        "is shorter than the minimum allowed length (7)."
    )
    logger.success("Registration failed as expected with error message")
