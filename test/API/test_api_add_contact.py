import pytest
from loguru import logger
from api_actions.api_contact_actions import ContActsApi
from api_actions.assert_json_response_body import assert_json_response
from api_actions.validate_response_schema import validate_response_schema
from test_data.contact_schemas import add_contact_response_schema
from test_data.contacts_data import (
    user_to_add_contact,
    new_contact_valid_data,
    new_contact_not_full_data,
    new_contact_empty_mandatory_fields,
    new_contact_invalid_data,
    invalid_phone,
    invalid_adress_data
)


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.api
def test_successfully_add_contact(clear_contacts):
    """
    Verifies, that the responce status code is 201,
    SignUp POST request is successful
    """
    newcont = ContActsApi()
    response = newcont.add_contact(
        user_to_add_contact,
        new_contact_valid_data)
    assert response.status_code == 201, \
        f'Status code is {response.status_code}, expected 201'
    assert_json_response(new_contact_valid_data, response.json())
    assert validate_response_schema(
        add_contact_response_schema,
        response.json()
    ), \
        f'Response schema does not match, got {response.json()}'
    logger.success('Contact is successfully added')


@pytest.mark.regression
@pytest.mark.api
def test_is_new_in_contact_list(clear_contacts):
    """
    Adds new contact, looks for new contact's ID among all contact IDs
    """
    newcont = ContActsApi()
    assert newcont.add_contact_and_check_is_added(
        user_to_add_contact,
        new_contact_valid_data), \
        "New contact's ID was not found"
    logger.success('New contact is successfully added to contact list')


@pytest.mark.regression
@pytest.mark.api
def test_add_cont_filling_only_mandatory_fields(clear_contacts):
    """
    Verifies Add new contact, filling only mandatory fields.
    Checks the response status code and JSON schema
    """
    newcont = ContActsApi()
    response = newcont.add_contact(
        user_to_add_contact,
        new_contact_not_full_data)
    assert response.status_code == 201, \
        f'Status code is {response.status_code}, expected 201'
    logger.success('Response status code is 201')
    assert validate_response_schema(
        add_contact_response_schema,
        response.json()
    ), f'Response schema does not match, got {response.json()}'
    logger.success('Got response json matches with expected schema')


@pytest.mark.regression
@pytest.mark.api
@pytest.mark.parametrize('body, description', new_contact_empty_mandatory_fields)
def test_add_contact_with_empty_mandatory_fields(body, description):
    """
    Tries to add new contact, missing mandatory fields
    """
    logger.info(f'Add contact with invalid data: {description}')
    newcont = ContActsApi()
    response = newcont.add_contact(user_to_add_contact, body)
    assert response.status_code == 400, \
        f'Status code is {response.status_code}, expected 400'
    logger.success('Addition of new contact failed with status code 400')


@pytest.mark.api
@pytest.mark.parametrize('body, description', new_contact_invalid_data)
def test_add_contact_with_invalid_common_data(body, description):
    """
    Tries to add new contact, using invalid birthdate, postal code, email
    """
    logger.info(f'Add contact with invalid data: {description}')
    newcont = ContActsApi()
    response = newcont.add_contact(user_to_add_contact, body)
    assert response.status_code == 400, \
        f'Status code is {response.status_code}, expected 400'
    logger.success('Addition of new contact failed with status code 400')


@pytest.mark.api
@pytest.mark.parametrize('body, description', invalid_phone)
def test_add_contact_with_invalid_phone(body, description):
    """
    Tries to add new contact with invalid phone number
    """
    logger.info(f'Add contact with invalid data: {description}')
    newcont = ContActsApi()
    response = newcont.add_contact(user_to_add_contact, body)
    assert response.status_code == 400, \
        f'Status code is {response.status_code}, expected 400'
    logger.success("Addition of new contact failed with status code 400. "
                   f"{response.json()['message']}")


@pytest.mark.api
@pytest.mark.xfail
@pytest.mark.parametrize('body, description', invalid_adress_data)
def test_add_contact_with_invalid_adress_data(body, description):
    """
    Tries to add new contact usind invalid names of city, or state, or country
    """
    logger.info(f'Add contact with invalid data: {description}')
    newcont = ContActsApi()
    response = newcont.add_contact(user_to_add_contact, body)
    assert response.status_code == 400, \
        f'Status code is {response.status_code}, expected 400'
    logger.success("Addition of new contact failed with status code 400")
