import pytest
from loguru import logger
from test_data.env import Env
from pages.login_page import LoginPage
from pages.api_add_user import AddUserApi
from test_data.user_creds import UserCredentials as UC
from test_data.register_data import invalid_email_ui, short_pasword_ui


def test_add_user_valid_creds(driver):
    """
    Verifies successful registration vith valid user credentials
    """
    logpage = LoginPage(driver, Env.URL_Login)
    logpage.open()
    add_usr_page = logpage.click_signup()
    assert add_usr_page.is_add_user_page()
    add_usr_page.add_new_user(UC.reg_new_fname, UC.reg_new_lname,
                              UC.reg_new_email, UC.reg_new_password)
    assert add_usr_page.if_signup_successful
    logger.success("New user is successfully added")
    rm = AddUserApi()
    rm.delete_user({"email": UC.reg_new_email,
                    "password": UC.reg_new_password})


def test_sign_up_user_exist(driver):
    """
    Verifies, that registration flops if user is already registered
    """
    logpage = LoginPage(driver, Env.URL_Login)
    logpage.open()
    add_usr_page = logpage.click_signup()
    assert add_usr_page.is_add_user_page()
    add_usr_page.add_new_user(UC.exist_usr_fname, UC.exist_usr_lname,
                              UC.exist_usr_email, UC.exist_usr_password)
    assert add_usr_page.is_error_text_correct(add_usr_page.err_registered_msg)
    logger.success("Registration failed as expected with error message")


def test_cancel_registration(driver):
    """
    Verifies returning to Login page after cancelling of Sign Up
    """
    logpage = LoginPage(driver, Env.URL_Login)
    logpage.open()
    add_usr_page = logpage.click_signup()
    assert add_usr_page.is_add_user_page()
    cancel = add_usr_page.cancel_add_user(UC.reg_new_fname, UC.reg_new_lname,
                                          UC.reg_new_email, UC.reg_new_password)
    assert cancel.is_url_correct(f'{Env.URL_Login}login')
    logger.success('Registration is successfully canceled')


def test_add_user_without_f_name(driver):
    """
    Verifies, that registration flops if [First Name] field is not filled
    """
    logpage = LoginPage(driver, Env.URL_Login)
    logpage.open()
    add_usr_page = logpage.click_signup()
    assert add_usr_page.is_add_user_page()
    add_usr_page.add_new_user(' ', UC.reg_new_lname, UC.reg_new_email, UC.reg_new_password)
    assert add_usr_page.is_error_text_correct(add_usr_page.err_fname_msg)
    logger.success("Registration failed as expected with error message")


def test_add_user_without_l_name(driver):
    """
    Verifies, that registration flops if [Last Name] field is not filled
    """
    logpage = LoginPage(driver, Env.URL_Login)
    logpage.open()
    add_usr_page = logpage.click_signup()
    assert add_usr_page.is_add_user_page()
    add_usr_page.add_new_user(UC.reg_new_fname, ' ', UC.reg_new_email, UC.reg_new_password)
    assert add_usr_page.is_error_text_correct(add_usr_page.err_lname_msg)
    logger.success("Registration failed as expected with error message")


@pytest.mark.parametrize('f_name, l_name, email, password, description', invalid_email_ui)
def test_add_user_with_invalid_email(driver, f_name, l_name, email, password, description):
    """
    Verifies, that registration flops if [Email] is empty or filled with incorrect data
    """
    logger.info(f'Test: registration with {description}')
    logpage = LoginPage(driver, Env.URL_Login)
    logpage.open()
    add_usr_page = logpage.click_signup()
    assert add_usr_page.is_add_user_page()
    add_usr_page.add_new_user(f_name, l_name, email, password)
    assert add_usr_page.is_error_text_correct(add_usr_page.err_email_msg)
    logger.success("Registration failed as expected with error message")


def test_add_user_without_password(driver):
    """
    Verifies, that registration flops if [Password] field is not filled
    """
    logpage = LoginPage(driver, Env.URL_Login)
    logpage.open()
    add_usr_page = logpage.click_signup()
    assert add_usr_page.is_add_user_page()
    add_usr_page.add_new_user(UC.reg_new_fname, UC.reg_new_password, UC.reg_new_email, ' ')
    assert add_usr_page.is_error_text_correct(add_usr_page.err_password_msg)
    logger.success("Registration failed as expected with error message")


@pytest.mark.parametrize('f_name, l_name, email, password', short_pasword_ui)
def test_add_user_short_password(driver, f_name, l_name, email, password):
    """
    Verifies, that registration flops if password contains less than 7 symbols
    """
    logger.info(f'Test: registration with password {password}')
    logpage = LoginPage(driver, Env.URL_Login)
    logpage.open()
    add_usr_page = logpage.click_signup()
    assert add_usr_page.is_add_user_page()
    add_usr_page.add_new_user(f_name, l_name, email, password)
    assert add_usr_page.is_error_text_correct(
        f"User validation failed: password: Path `password` (`{password}`) "
        "is shorter than the minimum allowed length (7)."
    )
    logger.success("Registration failed as expected with error message")
