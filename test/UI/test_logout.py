from loguru import logger
from test_data.env import Env
from pages.login_page import LoginPage
from test_data.edit_data import EditData
from test_data.user_creds import UserCredentials
from pages.add_contact_page import AddContactPage
from pages.edit_contact_page import EditContactPage
from pages.contact_list_page import ContactListPage
from pages.contact_details_page import ContactDetailsPage


def assert_logout(page):
    button = page.locate_element(page.logout_button)
    assert button.is_displayed(), f"The logout button {page.logout_button} is not visible."
    assert button.is_enabled(), f"The logout button {page.logout_button} is disabled."
    page.logout()
    assert page.is_url_correct(Env.URL_Login), \
        "User was not redirected to the Login page after logout."


def test_logout_button_on_contact_list_page(driver):
    # Navigate to the Contact List page
    contact_list = ContactListPage(driver, Env.URL_ContactList)
    contact_list_page = contact_list.navigate_to_contact_list_page(
        UserCredentials.it_email,
        UserCredentials.it_password)
    contact_list_page.is_contact_list_page()

    # Check the presence of the Logout button and the redirection to the Login page.
    assert_logout(contact_list_page)
    logger.success(
        "The Logout button is visible and enabled on the Contact List page. "
        "Clicking on the button redirects users to the Login page"
    )


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


def test_logout_button_on_contact_details_page(driver):
    # Navigate to the Contact Details page
    contact_details = ContactDetailsPage(driver, Env.URL_ContactDetails)
    contact_details_page = contact_details.navigate_to_contact_details_page(
        UserCredentials.it_email,
        UserCredentials.it_password)
    contact_details_page.is_contact_details_page()

    # Check the presence of the Logout button and the redirection to the Login page.
    assert_logout(contact_details_page)
    logger.success(
        "The Logout button is visible and enabled on the Contact Details page. "
        "Clicking on the button redirects users to the Login page"
    )


def test_logout_button_on_edit_contact_page(driver):
    # Create a contact and open the edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_email,
        UserCredentials.it_password,
        EditData.contact_data_only_mandatory
    )
    edit_page.is_edit_page()

    # Check the presence of the Logout button and the redirection to the Login page.
    assert_logout(edit_page)
    logger.success(
        "The Logout button is visible and enabled on the Edit Contact page. "
        "Clicking on the button redirects users to the Login page"
    )


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
