import pytest
from loguru import logger
from test_data.env import Env
from pages.add_contact_page import AddContactPage
from pages.login_page import LoginPage
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


def test_is_expected_element_present(driver):
    """
    Checks the presense of expected elements on the page
    """
    ac_page = AddContactPage(driver, Env.URL_AddContact)
    add_contact_page = ac_page.navigate_to_add_contact_page(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password
        )
    assert add_contact_page.is_text_correct(add_contact_page.elements['title'], 'Add Contact')
    for element, locator in add_contact_page.elements.items():
        if element == 'title':
            continue
        assert add_contact_page.is_element_present(locator)
    logger.success('All the expected elements are present')


def test_cancel_add_new_contact(driver):
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    contact_list_page = login_page.complete_login(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password,
    )
    add_contact_page = contact_list_page.navigate_to_add_contact_page()
    add_contact_page.fill_contact_form(new_contact_cancel_data)
    add_contact_page.cancel()
    assert add_contact_page.is_url_correct(Env.URL_ContactList), \
        f'Url is incorrect, got {driver.current_url}'
    is_added = add_contact_page.is_text_present(
        locator='td',
        text=f"{new_contact_cancel_data['firstName']} {new_contact_cancel_data['lastName']}"
    )
    assert is_added is False, 'Contact was added to contact list but should not'
    logger.success('Addition of new contact was cancelled')


def test_add_new_contact(driver, clear_contacts):
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
    is_added = add_contact_page.is_text_present(
        locator='td',
        text=f"{new_contact_valid_data['firstName']} {new_contact_valid_data['lastName']}"
    )
    assert is_added, 'Contact was not added to contact list'
    logger.success('New contact was successfully added')


def test_add_contact_filling_only_mandatory_fields(driver, clear_contacts):
    """
    Verifies Add new contact, filling only mandatory fields.
    """
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    contact_list_page = login_page.complete_login(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password,
    )
    add_contact_page = contact_list_page.navigate_to_add_contact_page()
    add_contact_page.fill_contact_form(new_contact_not_full_data)
    add_contact_page.submit()
    assert add_contact_page.is_url_correct(Env.URL_ContactList), \
        f'Url is incorrect, got {driver.current_url}'
    is_added = add_contact_page.is_text_present(
        locator='td',
        text=f"{new_contact_not_full_data['firstName']} {new_contact_not_full_data['lastName']}"
    )
    assert is_added, 'Contact was not added to contact list'
    logger.success('New contact was successfully added')


@pytest.mark.parametrize('new_cont, description, err_message', ui_new_cont_empty_mandatory_fields)
def test_add_contact_skip_mandatory_fields(driver, new_cont, description, err_message):
    """
    Tries to add new contact, missing mandatory fields
    """
    logger.info(f'Add contact with invalid data {description}')
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    contact_list_page = login_page.complete_login(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password,
    )
    add_contact_page = contact_list_page.navigate_to_add_contact_page()
    add_contact_page.fill_contact_form(new_cont)
    add_contact_page.submit()
    assert add_contact_page.is_error_text_correct(err_message)
    logger.success("Registration failed as expected with error message")


@pytest.mark.parametrize('new_contact, description, err_message',
                         ui_new_contact_invalid_data)
def test_add_contact_with_invalid_common_data(driver, new_contact, description, err_message):
    """
    Tries to add new contact, using invalid birthdate, postal code, email
    """
    logger.info(f'Add contact with invalid data {description}')
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    contact_list_page = login_page.complete_login(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password,
    )
    add_contact_page = contact_list_page.navigate_to_add_contact_page()
    add_contact_page.fill_contact_form(new_contact)
    add_contact_page.submit()
    assert add_contact_page.is_error_text_correct(err_message)
    logger.success("Registration failed as expected with error message")


@pytest.mark.parametrize('new_contact, description, err_message', ui_invalid_phone)
def test_add_contact_with_invalid_phone(driver, new_contact, description, err_message):
    """
    Tries to add new contact with invalid phone number
    """
    logger.info(f'Add contact with invalid data {description}')
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    contact_list_page = login_page.complete_login(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password,
    )
    add_contact_page = contact_list_page.navigate_to_add_contact_page()
    add_contact_page.fill_contact_form(new_contact)
    add_contact_page.submit()
    assert add_contact_page.is_error_text_correct(err_message)
    logger.success("Registration failed as expected with error message")


@pytest.mark.xfail(reason='Adress fields accept incorrect data')
@pytest.mark.parametrize('new_contact, description', invalid_adress_data)
def test_add_contact_with_invalid_adress(driver, new_contact, description):
    """
    Tries to add new contact usind invalid names of city, or state, or country
    """
    logger.info(f'Add contact with invalid data {description}')
    login_page = LoginPage(driver, Env.URL_Login)
    login_page.open()
    contact_list_page = login_page.complete_login(
        UC.user_to_add_contact_email,
        UC.user_to_add_contact_password,
    )
    add_contact_page = contact_list_page.navigate_to_add_contact_page()
    add_contact_page.fill_contact_form(new_contact)
    add_contact_page.submit()
    assert add_contact_page.is_text_present(
        locator='span',
        text='Contact validation failed'
    )
    logger.success("Registration failed as expected with error message")
