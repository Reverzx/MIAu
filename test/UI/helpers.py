from loguru import logger
from test_data.env import Env
from pages.login_page import LoginPage
from pages.contact_details_page import ContactDetailsPage


def navigate_contact_list_page(driver, email, password):
    """
    Logs in with the provided credentials and returns the Contact List page.
    :return: ContactListPage object
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    return login_page.complete_login(email, password)


def navigate_add_contact_page(driver, email, password):
    """
    Logs in with the provided credentials and navigates to the Add Contact page.
    :return: AddContactPage object
    """
    contact_list_page = navigate_contact_list_page(driver, email, password)
    return contact_list_page.navigate_to_add_contact_page()


def navigate_contact_details_page(driver, email, password):
    """
    Logs in with the provided credentials and navigates to the Contact Details page.
    :return: ContactDetailsPage object
    """
    contact_list_page = navigate_contact_list_page(driver, email, password)
    return contact_list_page.navigate_to_contact_details_page()


def navigate_edit_contact_page(driver, email, password):
    """
    Logs in with the provided credentials and navigates to the Edit Contact page.
    :return: EditContactPage object
    """
    contact_details_page = navigate_contact_details_page(driver, email, password)
    return contact_details_page.navigate_to_edit_contact_page()


def create_contact_and_navigate_edit_page(driver, email, password, contact_data):
    """
    Logs in using provided credentials, creates a contact using the given data,
    and navigates to the Edit Contact page.

    Steps:
    1. Open Login page and login.
    2. Navigate to Add Contact page and submit contact form.
    3. Navigate to Contact Details page, then to Edit Contact.

    :return: EditContactPage object
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    contact_list = login_page.complete_login(email, password)
    logger.info(
        "The user is logged in"
    )
    add_contact = contact_list.navigate_to_add_contact_page()
    add_contact.fill_contact_form(contact_data)
    add_contact.submit()
    logger.info(
        "A new contact is added."
    )
    contact_details = contact_list.navigate_to_contact_details_page()
    return contact_details.navigate_to_edit_contact_page()


def cancel_edit_and_delete_contact(edit_page):
    """
    Cancels editing on the Edit Contact page
    and deletes the contact from the Contact Details page.
    """
    edit_page.cancel()
    contact_upd = ContactDetailsPage(
        edit_page.driver,
        Env.URL_ContactDetails)
    contact_upd.delete_contact()
    logger.info("The contact is deleted")


def delete_contact(contact_details_page):
    """
    Deletes the contact from the Contact Details page.
    """
    contact_details_page.delete_contact()
    logger.info("The contact is deleted")


def assert_logout(page):
    button = page.locate_element(page.logout_button)
    assert button.is_displayed(), f"The logout button {page.logout_button} is not visible."
    assert button.is_enabled(), f"The logout button {page.logout_button} is disabled."
    page.logout()
    assert page.is_url_correct(Env.URL_Login),\
        "User was not redirected to the Login page after logout."
    