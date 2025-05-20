import pytest
from loguru import logger
from test_data.env import Env
from pages.add_contact_page import AddContactPage
from pages.login_page import LoginPage
from test_data.user_creds import UserCredentials as UC
from test_data.contacts_data import new_contact_not_full_data


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.ui
def test_return_to_contact_list_after_add_contact(driver, clear_contacts):
    addition = AddContactPage(driver, Env.URL_AddContact)
    addition.navigate_to_add_contact_page(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password
    )
    addition.fill_contact_form(new_contact_not_full_data)
    addition.submit()
    assert addition.is_url_correct(Env.URL_ContactList)
    logger.success('Successfully redirected to Contact List page')


@pytest.mark.ui
def test_return_without_add_contact(driver, clear_contacts):
    addition = AddContactPage(driver, Env.URL_AddContact)
    addition.navigate_to_add_contact_page(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password
    )
    addition.fill_contact_form(new_contact_not_full_data)
    addition.cancel()
    assert addition.is_url_correct(Env.URL_ContactList)
    logger.success('Successfully redirected to Contact List page')


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.ui
def test_return_after_clicking_return_button(driver, clear_contacts):
    addition = AddContactPage(driver, Env.URL_AddContact)
    addition.navigate_to_add_contact_page(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password
    )
    addition.fill_contact_form(new_contact_not_full_data)
    addition.submit()
    check = LoginPage(driver, Env.URL_Login)
    check.open()
    contact_list_page = check.complete_login(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password
    )
    contact_details_page = contact_list_page.navigate_to_contact_details_page()
    contact_details_page.click_return()
    assert contact_details_page.is_url_correct(Env.URL_ContactList)
