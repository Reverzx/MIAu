import pytest
from loguru import logger
from test_data.env import Env
from pages.login_page import LoginPage
from test_data.user_creds import UserCredentials


@pytest.mark.parametrize(
    "email, password",
    [
        (UserCredentials.zm_email, UserCredentials.zm_password),
    ],
)
def test_deleting_a_contact_positive_scenario(driver, email, password):
    """
    Verifies successful contact deletion with valid user credentials
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()

    contact_list_page = login_page.complete_login(email, password)
    assert contact_list_page.is_url_correct(Env.URL_ContactList), \
        f"Expected URL: {Env.URL_ContactList}, but return: {driver.current_url}"
    logger.info(
        "The user is logged in"
    )
    contact_details = contact_list_page.navigate_to_contact_details_page()
    assert contact_details is not None, "Don't open contact detail page - contact list is empty"
    contact_details.delete_contact()
    assert contact_list_page.is_url_correct(Env.URL_ContactList), \
        f"Expected URL: {Env.URL_ContactList}, but return: {driver.current_url}"
    logger.success("The contact has been successfully deleted and the user "
                   "has been redirected to the contact list")


@pytest.mark.parametrize(
    "email, password",
    [
        (UserCredentials.zm_email, UserCredentials.zm_password),
    ],
)
def test_deleting_a_contact_canceling(driver, email, password):
    """
    Verifies that clicking "Нет" in the delete confirmation popup cancels deletion
    and user stays on the contact details or contact list page.
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()

    contact_list_page = login_page.complete_login(email, password)
    assert contact_list_page.is_url_correct(Env.URL_ContactList), \
        f"Expected URL: {Env.URL_ContactList}, but return: {driver.current_url}"
    logger.info(
        "The user is logged in"
    )
    contact_details = contact_list_page.navigate_to_contact_details_page()
    assert contact_details is not None, "Don't open contact detail page - contact list is empty"
    contact_details.cancel_delete_contact()
    assert contact_list_page.is_url_correct(Env.URL_ContactDetails), \
        f"Expected URL: {Env.URL_ContactDetails}, but return: {driver.current_url}"
