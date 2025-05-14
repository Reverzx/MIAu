import pytest
import requests
from loguru import logger
from test_data.env import Env
from test_data.edit_data import EditData
from test_data.user_creds import UserCredentials
from api_actions.delete_contact import delete_contact
from api_actions.put_contact_upd import put_contact_upd
from api_actions.login_and_get_token import login_and_get_token
from api_actions.add_contact_and_get_id import add_contact_and_get_id
from api_actions.assert_json_response_body import assert_json_response
from api_actions.validate_response_schema import validate_response_schema


def test_successful_put_update(read_schema):
    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)
    payload = EditData.updated_data
    response = put_contact_upd(token, cont_id, payload)

    # Check the response status code
    assert response.status_code == 200, \
        f"Wrong status code: {response.status_code}. Expected: 200"

    # Check the response json data
    assert_json_response(EditData.updated_data, response.json())
    logger.success("Put request passed with response code 200. "
                   "The response body contains updated data")

    # Delete test data
    delete_contact(token, cont_id)


def test_put_contact_upd_response_schema(read_schema):
    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)
    payload = EditData.updated_data
    response = put_contact_upd(token, cont_id, payload)

    # Check the response schema
    schema = read_schema["put_contact_upd"]
    validate_response_schema(response, schema)
    logger.success("JSON-response corresponds to the schema.")

    # Delete test data
    delete_contact(token, cont_id)


def test_put_upd_fails_for_unauthorized_user():
    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)
    response = requests.put(
        f"{Env.URL_Login}contacts/{cont_id}",
        json=EditData.updated_data
    )

    # Check the response status code
    assert response.status_code == 401, \
        f"Wrong status code: {response.status_code}. Expected: 401"

    # Check the error
    assert response.json()["error"] == "Please authenticate.", \
        f"Missing or wrong error: {response.json()}. Expected: 'Please authenticate'."
    logger.success(f"Put request failed as expected."
                   f"Response status code is {response.status_code}."
                   f"Error message is {response.json()['error']}")

    # Delete test data
    delete_contact(token, cont_id)


@pytest.mark.parametrize('element_id, value, message', EditData.mandatory_fields_errors_api)
def test_put_upd_fails_with_missing_mandatory_data(element_id, value, message):
    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)

    payload = EditData.contact_data.copy()
    payload[element_id] = value
    response = put_contact_upd(token, cont_id, payload)

    # Check the response status code
    assert response.status_code == 400, \
        f"Wrong status code: {response.status_code}. Expected: 400"

    # Check the error
    assert response.json()["message"] == message
    logger.success(f"Put request failed as expected. "
                   f"Response status code is {response.status_code}. "
                   f"Error message is {response.json()['message']}.")

    # Delete test data
    delete_contact(token, cont_id)


def test_successful_put_upd_with_only_mandatory_data():
    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)

    # Only First Name and Last Name are provided
    payload = EditData.contact_data.copy()
    for key, value in payload.items():
        if key == "firstName" or key == "lastName":
            continue
        else:
            payload[key] = ""
    response = put_contact_upd(token, cont_id, EditData.updated_data)

    # Check the response status code
    assert response.status_code == 200, \
        f"Wrong status code: {response.status_code}. Expected: 200"
    logger.success(f"Put request passed with only mandatory fields in the payload. "
                   f"Response status code is {response.status_code}.")

    # Delete test data
    delete_contact(token, cont_id)


def test_successful_put_upd_with_max_allowed_chars_length():
    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)

    response = put_contact_upd(token, cont_id, EditData.max_length_allowed_filled)

    # Check the response status code
    assert response.status_code == 200, \
        f"Wrong status code: {response.status_code}. Expected: 200"
    logger.success(f"Put request passed with values at the maximum allowed character length. "
                   f"Response status code is {response.status_code}.")

    # Delete test data
    delete_contact(token, cont_id)


@pytest.mark.parametrize('element_id, value, message', EditData.max_length_exceeded)
def test_put_upd_fails_for_exceeded_max_chars_length(element_id, value, message):
    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)
    payload = EditData.contact_data.copy()
    payload[element_id] = value
    response = put_contact_upd(token, cont_id, payload)

    # Check the response status code
    assert response.status_code == 400, \
        f"Wrong status code: {response.status_code}. Expected: 400"

    # Check the error
    assert response.json()["message"] == message
    logger.success(f"Put request failed as expected "
                   f"with values exceeding the maximum allowed length. "
                   f"Response status code is {response.status_code}. "
                   f"Error message is {response.json()['message']}.")

    # Delete test data
    delete_contact(token, cont_id)


@pytest.mark.parametrize('value', EditData.valid_emails)
def test_successful_put_upd_for_valid_email(value):
    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)

    payload = EditData.contact_data.copy()
    payload["email"] = value

    response = put_contact_upd(token, cont_id, payload)

    # Check the response status code
    assert response.status_code == 200, \
        f"Wrong status code: {response.status_code}. Expected: 200"
    logger.success(f"Put request passed with valid email values. "
                   f"Response status code is {response.status_code}.")

    # Delete test data
    delete_contact(token, cont_id)


@pytest.mark.parametrize('value, description', EditData.invalid_emails)
def test_put_upd_fails_for_invalid_email(value, description):
    # Run PUT request to the /contacts endpoint
    logger.info(f"Test: Email address is edited with invalid value: {description}")
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)

    payload = EditData.contact_data.copy()
    payload["email"] = value

    response = put_contact_upd(token, cont_id, payload)

    # Check the response status code
    assert response.status_code == 400, \
        f"Wrong status code: {response.status_code}. Expected: 400"

    # Check the error
    assert response.json()["message"] == "Validation failed: email: Email is invalid", \
        (f"Wrong error message: {response.json()['message']}. "
         f"Expected: 'Validation failed: email: Email is invalid'")
    logger.success(f"Put request failed as expected with invalid email values. "
                   f"Response status code is {response.status_code}. "
                   f"Error message is {response.json()['message']}.")

    # Delete test data
    delete_contact(token, cont_id)


@pytest.mark.parametrize('value', EditData.valid_phones)
def test_successful_put_upd_for_valid_phone(value):
    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)

    payload = EditData.contact_data.copy()
    payload["phone"] = value

    response = put_contact_upd(token, cont_id, payload)

    # Check the response status code
    assert response.status_code == 200, \
        f"Wrong status code: {response.status_code}. Expected: 200"
    logger.success(f"Put request passed with valid phone values. "
                   f"Response status code is {response.status_code}.")

    # Delete test data
    delete_contact(token, cont_id)


@pytest.mark.parametrize('value', EditData.invalid_phones)
def test_put_upd_fails_for_invalid_phone(value):
    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)

    payload = EditData.contact_data.copy()
    payload["phone"] = value

    response = put_contact_upd(token, cont_id, payload)

    # Check the response status code
    assert response.status_code == 400, \
        f"Wrong status code: {response.status_code}. Expected: 400"

    # Check the error
    assert response.json()["message"] == "Validation failed: phone: Phone number is invalid", \
        (f"Wrong error message: {response.json()['message']}. "
         f"Expected: 'Validation failed: phone: Phone number is invalid'")
    logger.success(f"Put request failed as expected with invalid phone values. "
                   f"Response status code is {response.status_code}. "
                   f"Error message is {response.json()['message']}.")

    # Delete test data
    delete_contact(token, cont_id)


@pytest.mark.parametrize('value', EditData.valid_birthdate)
def test_successful_put_upd_for_valid_birthdate(value):
    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)

    payload = EditData.contact_data.copy()
    payload["birthdate"] = value

    response = put_contact_upd(token, cont_id, payload)

    # Check the response status code
    assert response.status_code == 200, \
        f"Wrong status code: {response.status_code}. Expected: 200"
    logger.success(f"Put request passed with valid birthdate values. "
                   f"Response status code is {response.status_code}.")

    # Delete test data
    delete_contact(token, cont_id)


@pytest.mark.parametrize('value, description', EditData.invalid_birthdate)
def test_put_upd_fails_for_invalid_birthdate(value, description):
    logger.info(f"Test: Birthdate is edited with invalid value: {description}")

    # Run PUT request to the /contacts endpoint
    token = login_and_get_token(UserCredentials.it_edit_email,
                                UserCredentials.it_edit_password)
    cont_id = add_contact_and_get_id(token, EditData.contact_data)

    payload = EditData.contact_data.copy()
    payload["birthdate"] = value

    response = put_contact_upd(token, cont_id, payload)

    # Check the response status code
    assert response.status_code == 400, \
        f"Wrong status code: {response.status_code}. Expected: 400"

    # Check the error
    assert response.json()["message"] == "Validation failed: birthdate: Birthdate is invalid", \
        (f"Wrong error message: {response.json()['message']}. "
         f"Expected: 'Validation failed: birthdate: Birthdate is invalid'")
    logger.success(f"Put request failed as expected with invalid birthdate values. "
                   f"Response status code is {response.status_code}. "
                   f"Error message is {response.json()['message']}.")

    # Delete test data
    delete_contact(token, cont_id)
