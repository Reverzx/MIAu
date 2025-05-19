import pytest
from loguru import logger
from test_data.env import Env
from pages.login_page import LoginPage
from test_data.user_creds import UserCredentials
from pages.add_contact_page import AddContactPage


def assert_logout(page):
    button = page.locate_element(page.logout_button)
    assert button.is_displayed(), f"The logout button {page.logout_button} is not visible."
    assert button.is_enabled(), f"The logout button {page.logout_button} is disabled."
    page.logout()
    assert page.is_url_correct(Env.URL_Login), \
        "User was not redirected to the Login page after logout."


@pytest.mark.ui
def test_logout_button_on_contact_list_page(driver, login_page):
    # Navigate to the Contact List page
    contact_list_page =  login_page.complete_login(
        UserCredentials.it_email,
        UserCredentials.it_password
    )
    contact_list_page.is_contact_list_page()

    # Check the presence of the Logout button and the redirection to the Login page.
    assert_logout(contact_list_page)
    logger.success(
        "The Logout button is visible and enabled on the Contact List page. "
        "Clicking on the button redirects users to the Login page"
    )


@pytest.mark.regression
@pytest.mark.ui
def test_logout_button_on_add_contact_page(driver):
    # Navigate to the Add Contact page
    add_contact = AddContactPage(driver, Env.URL_AddContact)
    add_contact.navigate_to_add_contact_page(
        UserCredentials.it_email,
        UserCredentials.it_password
    )
    add_contact.is_add_contact_page()

    # Check the presence of the Logout button and the redirection to the Login page.
    assert_logout(add_contact)
    logger.success(
        "The Logout button is visible and enabled on the Add Contact page. "
        "Clicking on the button redirects users to the Login page"
    )


@pytest.mark.regression
@pytest.mark.ui
def test_logout_button_on_contact_details_page(driver, login_page):
    # Navigate to the Contact Details page
    contact_list_page = login_page.complete_login(
        UserCredentials.it_email,
        UserCredentials.it_password
    )
    contact_details_page = contact_list_page.navigate_to_contact_details_page()
    contact_details_page.is_contact_details_page()

    # Check the presence of the Logout button and the redirection to the Login page.
    assert_logout(contact_details_page)
    logger.success(
        "The Logout button is visible and enabled on the Contact Details page. "
        "Clicking on the button redirects users to the Login page"
    )


@pytest.mark.regression
@pytest.mark.ui
def test_logout_button_on_edit_contact_page(driver, create_contact_and_locate_edit_page):
    # Create a contact and open the edit page
    edit_page = create_contact_and_locate_edit_page
    edit_page.is_edit_page()

    # Check the presence of the Logout button and the redirection to the Login page.
    assert_logout(edit_page)
    logger.success(
        "The Logout button is visible and enabled on the Edit Contact page. "
        "Clicking on the button redirects users to the Login page"
    )


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.ui
def test_login_after_logout(driver):
    # Login and navigate to the Contact List page
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    contact_list_page = login_page.complete_login(
        UserCredentials.it_email,
        UserCredentials.it_password
    )

    # Log out and check the redirect to the Login page
    contact_list_page.logout()
    assert contact_list_page.is_url_correct(Env.URL_Login)

    # Log in and check the redirect to the Contact List page
    contact_list_page = login_page.complete_login(
        UserCredentials.it_email,
        UserCredentials.it_password
    )
    assert contact_list_page.is_url_correct(Env.URL_ContactList)
    logger.success(
        "The user successfully logged in after logging out."
    )
