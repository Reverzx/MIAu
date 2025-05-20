import pytest
from loguru import logger

from pages.login_page import LoginPage
from test_data.contacts_data import new_contact_valid_data
from test_data.env import Env
from test_data.user_creds import UserCredentials as UC


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.ui
def test_deleting_a_contact_positive_scenario(driver):
    """
    Verifies successful contact deletion with valid user credentials
    """
    # Open contact list page and add contact
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    contact_list_page = login_page.complete_login(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password,
    )
    add_contact_page = contact_list_page.navigate_to_add_contact_page()
    add_contact_page.fill_contact_form(new_contact_valid_data)
    add_contact_page.submit()
    assert add_contact_page.is_url_correct(Env.URL_ContactList), \
        f'Url is incorrect, got {driver.current_url}'

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


@pytest.mark.regression
@pytest.mark.ui
def test_deleting_a_contact_canceling(driver):
    """
    Verifies that clicking "Нет" in the delete confirmation popup cancels deletion
    and user stays on the contact details or contact list page.
    """
    # Open contact list page and add contact
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    contact_list_page = login_page.complete_login(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password,
    )
    add_contact_page = contact_list_page.navigate_to_add_contact_page()
    add_contact_page.fill_contact_form(new_contact_valid_data)
    add_contact_page.submit()
    assert add_contact_page.is_url_correct(Env.URL_ContactList), \
        f'Url is incorrect, got {driver.current_url}'

    # Navigate to details contact
    contact_details_page = contact_list_page.navigate_to_contact_details_page()
    assert contact_details_page is not None, ("Don't open contact detail page - "
                                              "contact list is empty")

    # Try deleted contact and canceling delete
    contact_details_page.cancel_delete_contact()
    assert contact_list_page.is_url_correct(Env.URL_ContactDetails), \
        f"Expected URL: {Env.URL_ContactDetails}, but return: {driver.current_url}"
