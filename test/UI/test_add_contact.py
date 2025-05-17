import pytest
from loguru import logger
from test_data.env import Env
from pages.add_contact_page import AddContactPage
from test_data.user_creds import UserCredentials as UC
from test_data.contacts_data import (
    new_contact_cancel_data,
    new_contact_valid_data,
    new_contact_not_full_data,
    ui_new_cont_empty_mandatory_fields,
    ui_new_contact_invalid_data,
    ui_invalid_phone,
    invalid_adress_data
)


def test_expected_element_present(driver):
    ac_page = AddContactPage(driver, Env.URL_AddContact)
    add_cont_page = ac_page.navigate_to_add_contact_page(
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password
        )
    assert add_cont_page.is_text_correct(add_cont_page.elements['title'], 'Add Contact')
    for element, locator in add_cont_page.elements.items():
        if element == 'title':
            continue
        assert add_cont_page.is_element_present(locator)
    logger.success('All the expected elements are present')


def test_cancel_add_cont(driver):
    addition = AddContactPage(driver, Env.URL_AddContact)
    result = addition.login_and_cancel_add_contact(
        driver,
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password,
        new_contact_cancel_data
    )
    assert result.is_url_correct(Env.URL_ContactList)
    is_added = result.is_text_present(
        locator='td',
        text=f"{new_contact_cancel_data['firstName']} {new_contact_cancel_data['lastName']}"
    )
    assert is_added is False


def test_add_new_cont(driver, clear_contacts):
    addition = AddContactPage(driver, Env.URL_AddContact)
    result = addition.login_and_add_contact(
        driver,
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password,
        new_contact_valid_data
    )
    assert result.is_url_correct(Env.URL_ContactList)
    is_added = result.is_text_present(
        locator='td',
        text=f"{new_contact_valid_data['firstName']} {new_contact_valid_data['lastName']}"
    )
    assert is_added


def test_add_cont_fill_only_mandatory_fields(driver, clear_contacts):
    addition = AddContactPage(driver, Env.URL_AddContact)
    result = addition.login_and_add_contact(
        driver,
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password,
        new_contact_not_full_data
    )
    assert result.is_url_correct(Env.URL_ContactList)
    is_added = result.is_text_present(
        locator='td',
        text=f"{new_contact_not_full_data['firstName']} {new_contact_not_full_data['lastName']}"
    )
    assert is_added


@pytest.mark.parametrize('new_cont, description, err_message', ui_new_cont_empty_mandatory_fields)
def test_add_contact_skip_mandatory_fields(driver, new_cont, description, err_message):
    logger.info(f'Add contact with invalid data {description}')
    addition = AddContactPage(driver, Env.URL_AddContact)
    addition.login_and_add_contact(
        driver,
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password,
        new_cont
    )
    assert addition.is_error_text_correct(err_message)
    logger.success("Registration failed as expected with error message")


@pytest.mark.parametrize('new_cont, description, err_message', ui_new_contact_invalid_data)
def test_add_contact_with_invalid_common_data(driver, new_cont, description, err_message):
    logger.info(f'Add contact with invalid data {description}')
    addition = AddContactPage(driver, Env.URL_AddContact)
    addition.login_and_add_contact(
        driver,
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password,
        new_cont
    )
    assert addition.is_error_text_correct(err_message)
    logger.success("Registration failed as expected with error message")


@pytest.mark.parametrize('new_cont, description, err_message', ui_invalid_phone)
def test_add_contact_with_invalid_phone(driver, new_cont, description, err_message):
    logger.info(f'Add contact with invalid data {description}')
    addition = AddContactPage(driver, Env.URL_AddContact)
    addition.login_and_add_contact(
        driver,
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password,
        new_cont
    )
    assert addition.is_error_text_correct(err_message)
    logger.success("Registration failed as expected with error message")


@pytest.mark.xfail
@pytest.mark.parametrize('new_cont, description', invalid_adress_data)
def test_add_contact_with_invalid_adress(driver, new_cont, description):
    logger.info(f'Add contact with invalid data {description}')
    addition = AddContactPage(driver, Env.URL_AddContact)
    addition.login_and_add_contact(
        driver,
        UC.usr_to_add_cont_email,
        UC.usr_to_add_cont_password,
        new_cont
    )
    assert addition.is_text_present(
        locator='span',
        text='Contact validation failed'
    )
    logger.success("Registration failed as expected with error message")
