import pytest
from loguru import logger
from test_data.env import Env
from test_data.user_creds import UserCredentials
from pages.login_page import LoginPage
from pages.contact_details_page import ContactDetailsPage
from test_data.edit_data import EditData
from selenium.webdriver.common.by import By


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
    contact_upd = ContactDetailsPage(edit_page.driver, Env.URL_ContactDetails)
    contact_upd.delete_contact()
    logger.info("The contact is deleted")


def delete_contact(contact_details_page):
    """
    Deletes the contact from the Contact Details page.
    """
    contact_details_page.delete_contact()
    logger.info("The contact is deleted")


def test_expected_elements_present(driver):
    """
    Verifies that expected title, fields, buttons are present
    on the Edit Contact page.

    A test contact is created before the test and deleted after the test.
    """
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_email,
        UserCredentials.it_password,
        EditData.contact_data_only_mandatory
    )
    assert edit_page.is_text_correct(edit_page.elements['title'], 'Edit Contact')
    for label, locator in edit_page.elements.items():
        if label == 'title':
            continue
        assert edit_page.is_element_present(locator)
    logger.success(
        "The expected elements are present on the Edit Contact page"
    )
    cancel_edit_and_delete_contact(edit_page)


def test_successful_edit_and_check_updated_details(driver):
    """
    Verifies that contact details can be successfully updated using valid data.
    Ensures that after submission the updated details are correctly displayed
    on the Contact Details page.

    A test contact is created before the test and deleted after the test.
    """
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_email,
        UserCredentials.it_password,
        EditData.contact_data
    )
    edit_page.edit_contact_form(EditData.updated_data)
    edit_page.submit()
    edit_page.is_url_correct(Env.URL_ContactDetails)
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    contact_upd.assert_contact_details_are_correct(EditData.updated_data)
    logger.success(
        "The contact is successfully edited. Contact details are correctly displayed"
    )
    contact_upd.delete_contact()


def test_cancel_edit(driver):
    """
    Verifies that edit contact can be canceled.
    Ensures that after cancelling the contact details are not changed
    on the Contact Details page.

    A test contact is created before the test and deleted after the test.
    """
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data
    )
    edit_page.edit_contact_form(EditData.updated_data)
    edit_page.cancel()
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    contact_upd.is_url_correct(Env.URL_ContactDetails)
    contact_upd.assert_contact_details_are_correct(EditData.contact_data)
    logger.success(
        "The edit is cancelled. Contact details are not changed"
    )
    contact_upd.delete_contact()


@pytest.mark.parametrize('element_id, value, message', EditData.max_length_exceeded)
def test_error_for_exceeded_max_chars_length(driver, element_id, value, message):
    """
    Verifies that an appropriate error message is displayed
    when fields are populated with values exceeding the maximum allowed length.

    A test contact is created before the test and deleted after the test.
    """
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )
    edit_page.input_text((By.ID, element_id), value)
    edit_page.submit()
    assert edit_page.is_error_displayed(message)
    logger.success(
        "The correct error message is displayed for fields populated "
        "with values exceeding the maximum allowed length."
    )
    cancel_edit_and_delete_contact(edit_page)


def test_successful_edit_with_max_allowed_chars_length(driver):
    """
    Verifies that no error message is displayed
    and the user is redirected to the Contact Details page
    when fields are edited with values at the maximum allowed character length.

    A test contact is created before the test and deleted after the test.
    """
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )
    edit_page.fill_fields_with_max_length_allowed()
    edit_page.submit_and_wait()
    assert edit_page.is_edit_successful()
    logger.success(
        "The contact is successfully edited "
        "with values at the maximum allowed character length"
    )
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    delete_contact(contact_upd)


@pytest.mark.parametrize('value, description', EditData.invalid_emails)
def test_error_for_invalid_email(driver, value, description):
    """
    Verifies that an appropriate error message is displayed
    when the email field is populated with invalid data.

    A test contact is created before the test and deleted after the test.
    """
    logger.info(f"Test: Email address is edited with invalid value: {description}")
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )
    edit_page.input_text(edit_page.elements['email'], value)
    edit_page.submit()
    assert edit_page.is_error_displayed(EditData.error_message['email'])
    logger.success(
        "The correct error message is displayed for the email field "
        "populated with invalid data."
    )
    cancel_edit_and_delete_contact(edit_page)


@pytest.mark.parametrize('value', EditData.valid_emails)
def test_successful_edit_with_valid_email(driver, value):
    """
    Verifies that no error message is displayed
    and the user is redirected to the Contact Details page
    when the email field is populated with valid data.

    A test contact is created before the test and deleted after the test.
    """
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )
    edit_page.input_text(edit_page.elements['email'], value)
    edit_page.submit_and_wait()
    assert edit_page.is_edit_successful()
    logger.success(
        "The contact is successfully edited "
        "with the email field populated with valid data."
    )
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    delete_contact(contact_upd)


@pytest.mark.parametrize('element_id, message', EditData.mandatory_fields_errors)
def test_error_for_not_populated_mandatory_fields(driver, element_id, message):
    """
    Verifies that an appropriate error message is displayed
    when the mandatory fields (First Name, Last name) are not populated.

    A test contact is created before the test and deleted after the test.
    """
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )
    edit_page.clear_field(element_id)
    edit_page.submit()
    assert edit_page.is_error_displayed(message)
    logger.success(
        "The correct error message is displayed for missing mandatory fields"
    )
    cancel_edit_and_delete_contact(edit_page)


@pytest.mark.parametrize('value', EditData.invalid_phones)
def test_error_for_invalid_phone(driver, value):
    """
    Verifies that an appropriate error message is displayed
    when the phone field is populated with invalid data.

    A test contact is created before the test and deleted after the test.
    """
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )
    edit_page.input_text(edit_page.elements['phone'], value)
    edit_page.submit()
    assert edit_page.is_error_displayed(EditData.error_message['phone'])
    logger.success(
        "The correct error message is displayed for the phone field "
        "populated with invalid data."
    )
    cancel_edit_and_delete_contact(edit_page)


@pytest.mark.parametrize('value', EditData.valid_phones)
def test_successful_edit_with_valid_phone(driver, value):
    """
    Verifies that no error message is displayed
    and the user is redirected to the Contact Details page
    when the phone field is populated with valid data.

    A test contact is created before the test and deleted after the test.
    """
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )
    edit_page.input_text(edit_page.elements['phone'], value)
    edit_page.submit_and_wait()
    assert edit_page.is_edit_successful()
    logger.success(
        "The contact is successfully edited "
        "with the phone field populated with valid data."
    )
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    delete_contact(contact_upd)


@pytest.mark.parametrize('value, description', EditData.invalid_birthdate)
def test_error_for_invalid_birthdate(driver, value, description):
    """
    Verifies that an appropriate error message is displayed
    when the birthdate field is populated with invalid data.

    A test contact is created before the test and deleted after the test.
    """
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )
    edit_page.input_text(edit_page.elements['birthdate'], value)
    edit_page.submit()
    assert edit_page.is_error_displayed(EditData.error_message['birthdate'])
    logger.success(
        "The correct error message is displayed for the birthdate field "
        "populated with invalid data."
    )
    cancel_edit_and_delete_contact(edit_page)


@pytest.mark.parametrize('value', EditData.valid_birthdate)
def test_successful_edit_with_valid_birthdate(driver, value):
    """
    Verifies that no error message is displayed
    and the user is redirected to the Contact Details page
    when the birthdate field is populated with valid data.

    A test contact is created before the test and deleted after the test.
    """
    edit_page = create_contact_and_navigate_edit_page(
        driver,
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )
    edit_page.input_text(edit_page.elements['birthdate'], value)
    edit_page.submit_and_wait()
    assert edit_page.is_edit_successful()
    logger.success(
        "The contact is successfully edited "
        "with the birthdate field populated with valid data."
    )
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    delete_contact(contact_upd)
