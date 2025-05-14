import pytest
from loguru import logger
from test_data.env import Env
from test_data.edit_data import EditData
from selenium.webdriver.common.by import By
from test_data.user_creds import UserCredentials
from pages.edit_contact_page import EditContactPage
from pages.contact_details_page import ContactDetailsPage


def test_expected_elements_present(driver):
    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )

    # Checking page elements
    assert edit_page.is_text_correct(edit_page.elements['title'], 'Edit Contact')

    for label, locator in edit_page.elements.items():
        if label == 'title':
            continue
        assert edit_page.is_element_present(locator), \
            "Expected element is not present on the Edit Contact page."
    logger.success(
        "The expected elements are present on the Edit Contact page"
    )

    # Delete test data
    edit_page.cancel_edit_and_delete_contact()


def test_successful_edit_and_check_updated_details(driver):
    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )

    # Edit contact and submit
    edit_page.edit_contact_form(EditData.updated_data)
    edit_page.submit()

    # Check redirect to the Contact Details page
    edit_page.is_url_correct(Env.URL_ContactDetails)

    # Check contact details are updated
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    contact_upd.assert_contact_details_are_correct(EditData.updated_data)
    logger.success(
        "The contact is successfully edited. Contact details are correctly displayed"
    )

    # Delete test data
    contact_upd.delete_contact()


def test_cancel_edit(driver):
    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data
    )

    # Edit contact and cancel
    edit_page.edit_contact_form(EditData.updated_data)
    edit_page.cancel()

    # Check contact details are not changed
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    contact_upd.is_url_correct(Env.URL_ContactDetails)
    contact_upd.assert_contact_details_are_correct(EditData.contact_data)
    logger.success(
        "The edit is cancelled. Contact details are not changed"
    )

    # Delete test data
    contact_upd.delete_contact()


@pytest.mark.parametrize('element_id, data, message', EditData.max_length_exceeded)
def test_error_for_exceeded_max_chars_length(driver, element_id, data, message):
    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )

    # Edit contact and submit
    edit_page.input_text((By.ID, element_id), data)
    edit_page.submit()

    # Check the error
    assert edit_page.is_error_displayed(message), "Error message is not displayed."
    logger.success(
        "The correct error message is displayed for fields populated "
        "with values exceeding the maximum allowed length."
    )

    # Delete test data
    edit_page.cancel_edit_and_delete_contact()


def test_successful_edit_with_max_allowed_chars_length(driver):
    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )

    # Edit contact and submit
    edit_page.fill_fields_with_max_length_allowed()
    edit_page.submit_and_wait()

    # Check the contact is updated
    assert edit_page.is_edit_successful()
    logger.success(
        "The contact is successfully edited "
        "with values at the maximum allowed character length"
    )

    # Delete test data
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    contact_upd.delete_contact()


@pytest.mark.parametrize('data, description', EditData.invalid_emails)
def test_error_for_invalid_email(driver, data, description):
    logger.info(f"Test: Email address is edited with invalid value: {description}")

    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )

    # Edit contact and submit
    edit_page.input_text(edit_page.elements['email'], data)
    edit_page.submit()

    # Check the error
    assert edit_page.is_error_displayed(EditData.error_message['email'])
    logger.success(
        "The correct error message is displayed for the email field "
        "populated with invalid data."
    )

    # Delete test data
    edit_page.cancel_edit_and_delete_contact()


@pytest.mark.parametrize('data', EditData.valid_emails)
def test_successful_edit_with_valid_email(driver, data):
    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )

    # Edit contact and submit
    edit_page.input_text(edit_page.elements['email'], data)
    edit_page.submit_and_wait()

    # Check the contact is updated
    assert edit_page.is_edit_successful()
    logger.success(
        "The contact is successfully edited "
        "with the email field populated with valid data."
    )

    # Delete test data
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    contact_upd.delete_contact()


@pytest.mark.parametrize('element_id, message', EditData.mandatory_fields_errors)
def test_error_for_not_populated_mandatory_fields(driver, element_id, message):
    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )

    # Edit contact and submit
    edit_page.clear_field(element_id)
    edit_page.submit()

    # Check the error
    assert edit_page.is_error_displayed(message)
    logger.success(
        "The correct error message is displayed for missing mandatory fields"
    )

    # Delete test data
    edit_page.cancel_edit_and_delete_contact()


@pytest.mark.parametrize('data', EditData.invalid_phones)
def test_error_for_invalid_phone(driver, data):
    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )

    # Edit contact and submit
    edit_page.input_text(edit_page.elements['phone'], data)
    edit_page.submit()

    # Check the error
    assert edit_page.is_error_displayed(EditData.error_message['phone'])
    logger.success(
        "The correct error message is displayed for the phone field "
        "populated with invalid data."
    )

    # Delete test data
    edit_page.cancel_edit_and_delete_contact()


@pytest.mark.parametrize('data', EditData.valid_phones)
def test_successful_edit_with_valid_phone(driver, data):
    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )

    # Edit contact and submit
    edit_page.input_text(edit_page.elements['phone'], data)
    edit_page.submit_and_wait()

    # Check the contact is updated
    assert edit_page.is_edit_successful()
    logger.success(
        "The contact is successfully edited "
        "with the phone field populated with valid data."
    )

    # Delete test data
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    contact_upd.delete_contact()


@pytest.mark.parametrize('data, description', EditData.invalid_birthdate)
def test_error_for_invalid_birthdate(driver, data, description):
    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )

    # Edit contact and submit
    edit_page.input_text(edit_page.elements['birthdate'], data)
    edit_page.submit()

    # Check the error
    assert edit_page.is_error_displayed(EditData.error_message['birthdate'])
    logger.success(
        "The correct error message is displayed for the birthdate field "
        "populated with invalid data."
    )

    # Delete test data
    edit_page.cancel_edit_and_delete_contact()


@pytest.mark.parametrize('data', EditData.valid_birthdate)
def test_successful_edit_with_valid_birthdate(driver, data):
    # Create contact and open edit page
    edit_page = EditContactPage(driver, Env.URL_EditContact)
    edit_page.create_contact_and_navigate_edit_page(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password,
        EditData.contact_data_only_mandatory
    )

    # Edit contact and submit
    edit_page.input_text(edit_page.elements['birthdate'], data)
    edit_page.submit_and_wait()

    # Check the contact is updated
    assert edit_page.is_edit_successful()
    logger.success(
        "The contact is successfully edited "
        "with the birthdate field populated with valid data."
    )

    # Delete test data
    contact_upd = ContactDetailsPage(driver, Env.URL_ContactDetails)
    contact_upd.delete_contact()
