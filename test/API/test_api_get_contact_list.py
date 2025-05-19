import pytest
from loguru import logger
from api_actions.api_contact_actions import ContActsApi
from test_data.contacts_data import (user_without_cont as usr_empty,
                                     user_to_add_contact as user, new_contact_valid_data as ncvd)
from test_data.edit_data import EditData


@pytest.mark.api
def test_get_contacts_when_no_contacts_created():

    # User authorization without contacts
    contact_api = ContActsApi()
    header = contact_api.auth_and_get_token(usr_empty)

    # Getting the contact list (GET)
    response = contact_api.req_get_contact_list(header)

    # Checking status code 200
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Checking list is empty
    assert response.json() == [], f"Expected empty list, got: {response.json()}"
    logger.success("The expected status code 200 has been received and "
                   "response is an empty list []")


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.api
def test_get_contacts_when_contacts_created():

    # User authorization with contacts
    contact_api = ContActsApi()
    header = contact_api.auth_and_get_token(user)

    # Checking contact list. If contact list is empty, create new contact
    response_list = contact_api.req_get_contact_list(header)
    if response_list.status_code == 200 and len(response_list.json()) == 0:
        response_add = contact_api.req_add_contact(ncvd, header)
        assert response_add.status_code == 201

    # Checking contact list
    response = contact_api.req_get_contact_list(header)
    contacts = response.json()
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Checking all fields for contact
    required_fields = ["_id", "firstName", "lastName", "birthdate", "email",
                       "phone", "street1", "street2", "city", "stateProvince",
                       "postalCode", "country", "owner", "__v"]
    for field in required_fields:
        assert field in contacts[0], f"Field '{field}' is missing in contact: {contacts[0]}"

    logger.success("The expected status code 200 has been received "
                   "and response contains contacts with all required fields.")


@pytest.mark.api
def test_get_and_add_contact():

    # User authorization
    contact_api = ContActsApi()
    header = contact_api.auth_and_get_token(user)

    # Create contact
    response_add = contact_api.req_add_contact(ncvd, header)
    assert response_add.status_code == 201
    cont_id = response_add.json()["_id"]

    # Checking contact ID
    response_get = contact_api.req_get_contact(cont_id, header)
    assert response_get.status_code == 200, f"Expected 200, got {response_get.status_code}"
    logger.success("The contact has been successfully created and retrieved by ID")

    # Finale clear
    try:
        contact_api.delete_contact(header, cont_id)
    except Exception as e:
        logger.warning(f"Error message: {e}")


@pytest.mark.api
def test_get_and_delete_contact():

    # User authorization
    contact_api = ContActsApi()
    header = contact_api.auth_and_get_token(user)

    # Create contact
    response_add = contact_api.req_add_contact(ncvd, header)
    assert response_add.status_code == 201
    cont_id = response_add.json()["_id"]

    # Delete contact
    response_delete = contact_api.delete_contact(header, cont_id)
    assert response_delete.status_code == 200, f"Expected 200, got {response_delete.status_code}"

    # Checking deleted contact ID
    response_get = contact_api.req_get_contact(cont_id, header)
    assert response_get.status_code == 404, f"Expected 404, got {response_get.status_code}"
    logger.success("The expected status code 404 has been received when "
                   "trying to get a deleted contact")


@pytest.mark.regression
@pytest.mark.api
def test_get_updated_contact():

    # User authorization
    contact_api = ContActsApi()
    header = contact_api.auth_and_get_token(user)

    # Create contact
    response_add = contact_api.req_add_contact(ncvd, header)
    assert response_add.status_code == 201
    cont_id = response_add.json()["_id"]

    # Update contact (PATCH /contacts/{id})
    updated_data = EditData.updated_data
    response_upd = contact_api.req_patch_upd_contact(cont_id, updated_data, header)
    assert response_upd.status_code == 200, f"Expected 200, got {response_upd.status_code}"

    # Checking contact (GET /contacts/{id})
    response_get = contact_api.req_get_contact(cont_id, header)
    assert response_get.status_code == 200, f"Expected 200, got {response_get.status_code}"

    # Checking data upd contact
    contact = response_get.json()
    assert contact["firstName"] == updated_data["firstName"]
    assert contact["lastName"] == updated_data["lastName"]
    assert contact["birthdate"] == updated_data["birthdate"]
    assert contact["email"] == updated_data["email"]
    assert contact["phone"] == updated_data["phone"]
    logger.success("The contact has been successfully updated and "
                   "the response contains updated data")

    # Finale clear
    try:
        contact_api.delete_contact(header, cont_id)
    except Exception as e:
        logger.warning(f"Error message: {e}")
