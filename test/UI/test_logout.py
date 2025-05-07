from loguru import logger
from test_data.env import Env
from test_data.user_creds import UserCredentials
from pages.login_page import LoginPage
from test.UI.helpers import (
    navigate_contact_list_page,
    navigate_add_contact_page,
    navigate_contact_details_page,
    navigate_edit_contact_page,
    assert_logout
)


def test_logout_button_on_contact_list_page(driver):
    """
    Verifies the Logout button is visible and clickable on the Contact List page.
    Ensure the user is redirected to the Login page when clicking the Logout button.
    """
    contact_list_page = navigate_contact_list_page(
        driver,
        UserCredentials.it_email,
        UserCredentials.it_password
    )
    assert_logout(contact_list_page)
    logger.success(
        "The Logout button is visible and enabled on the Contact List page. "
        "Clicking on the button redirects users to the Login page"
    )


def test_logout_button_on_add_contact_page(driver):
    """
    Verifies the Logout button is visible and clickable on the Add Contact page.
    Ensure the user is redirected to the Login page when clicking the Logout button.
    """
    add_contact_page = navigate_add_contact_page(
        driver,
        UserCredentials.it_email,
        UserCredentials.it_password
    )
    assert_logout(add_contact_page)
    logger.success(
        "The Logout button is visible and enabled on the Add Contact page. "
        "Clicking on the button redirects users to the Login page"
    )


def test_logout_button_on_contact_details_page(driver):
    """
    Verifies the Logout button is visible and clickable on the Contact Details page.
    Ensure the user is redirected to the Login page when clicking the Logout button.
    """
    contact_details_page = navigate_contact_details_page(
        driver,
        UserCredentials.it_email,
        UserCredentials.it_password
    )
    assert_logout(contact_details_page)
    logger.success(
        "The Logout button is visible and enabled on the Contact Details page. "
        "Clicking on the button redirects users to the Login page"
    )


def test_logout_button_on_edit_contact_page(driver):
    """
    Verifies the Logout button is visible and clickable on the Edit Contact page.
    Ensure the user is redirected to the Login page when clicking the Logout button.
    """
    edit_contact_page = navigate_edit_contact_page(
        driver,
        UserCredentials.it_email,
        UserCredentials.it_password
    )
    assert_logout(edit_contact_page)
    logger.success(
        "The Logout button is visible and enabled on the Edit Contact page. "
        "Clicking on the button redirects users to the Login page"
    )


def test_login_after_logout(driver):
    """
    Verifies that after logout a user can successfully log in back to the application.
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    contact_list_page = login_page.complete_login(
        UserCredentials.it_email,
        UserCredentials.it_password
    )
    contact_list_page.logout()
    assert contact_list_page.is_url_correct(Env.URL_Login)
    contact_list_page = login_page.complete_login(
        UserCredentials.it_email,
        UserCredentials.it_password
    )
    assert contact_list_page.is_url_correct(Env.URL_ContactList)
    logger.success(
        "The user successfully logged in after logging out."
    )
