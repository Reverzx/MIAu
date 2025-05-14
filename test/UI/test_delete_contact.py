from loguru import logger
from test_data.env import Env
from pages.add_contact_page import AddContactPage
from test_data.user_creds import UserCredentials as UC
from test_data.contacts_data import new_cont_valid_data as ncvd


def test_deleting_a_contact_positive_scenario(driver):
    """
    Verifies successful contact deletion with valid user credentials
    """
    # Open contact list page and add contact
    addition = AddContactPage(driver, Env.URL_AddContact)
    contact_list_page = addition.login_and_add_contact(
        driver,
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password,
        ncvd
    )
    assert contact_list_page.is_url_correct(Env.URL_ContactList)

    # Navigate to details contact
    contact_details_page = contact_list_page.navigate_to_contact_details_page()
    assert contact_details_page is not None, ("Don't open contact detail page - "
                                              "contact list is empty")

    # Delete contact and redirect to the contact list
    contact_details_page.delete_contact()
    assert contact_details_page.is_url_correct(Env.URL_ContactList), \
        f"Expected URL: {Env.URL_ContactList}, but return: {driver.current_url}"
    logger.success("The contact has been successfully deleted and the user "
                   "has been redirected to the contact list")


def test_deleting_a_contact_canceling(driver):
    """
    Verifies that clicking "Нет" in the delete confirmation popup cancels deletion
    and user stays on the contact details or contact list page.
    """
    # Open contact list page and add contact
    addition = AddContactPage(driver, Env.URL_AddContact)
    contact_list_page = addition.login_and_add_contact(
        driver,
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password,
        ncvd
    )
    assert contact_list_page.is_url_correct(Env.URL_ContactList)

    # Navigate to details contact
    contact_details_page = contact_list_page.navigate_to_contact_details_page()
    assert contact_details_page is not None, ("Don't open contact detail page - "
                                              "contact list is empty")

    # Try deleted contact and canceling delete
    contact_details_page.cancel_delete_contact()
    assert contact_list_page.is_url_correct(Env.URL_ContactDetails), \
        f"Expected URL: {Env.URL_ContactDetails}, but return: {driver.current_url}"
