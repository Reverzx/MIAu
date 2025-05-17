import pytest
from loguru import logger
from test_data.env import Env
from pages.add_contact_page import AddContactPage
from test_data.user_creds import UserCredentials as UC
from test_data.contacts_data import new_contact_not_full_data


def test_return_to_contact_list_after_add_contact(driver, clear_contacts):
    addition = AddContactPage(driver, Env.URL_AddContact)
    addition.navigate_to_add_contact_page(
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password
    )
    addition.fill_contact_form(new_contact_not_full_data)
    addition.submit()
    assert addition.is_url_correct(Env.URL_ContactList)
    logger.success('Successfully redirected to Contact List page')


def test_return_without_add_contact(driver, clear_contacts):
    addition = AddContactPage(driver, Env.URL_AddContact)
    addition.navigate_to_add_contact_page(
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password
    )
    addition.fill_contact_form(new_contact_not_full_data)
    addition.cancel()
    assert addition.is_url_correct(Env.URL_ContactList)
    logger.success('Successfully redirected to Contact List page')


def test_return_after_clicking_return_button(driver, clear_contacts):
    addition = AddContactPage(driver, Env.URL_AddContact)
    cl_page = addition.login_and_add_contact(
        driver,
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password,
        new_contact_not_full_data
    )
    cd_page = cl_page.navigate_to_contact_details_page()
    cd_page.click_return()
    assert cd_page.is_url_correct(Env.URL_ContactList)
