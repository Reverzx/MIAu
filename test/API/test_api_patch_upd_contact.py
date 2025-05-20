import pytest
from loguru import logger
from api_actions.api_contact_actions import ContActsApi
from test_data.edit_data import EditData
from test_data.contacts_data import user_to_add_contact as usr, new_contact_valid_data as ncvd


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.api
def test_update_contact_with_valid_data():
    # Create contact
    contact_api = ContActsApi()
    auth_header = contact_api.auth_and_get_header(usr)
    response_add = contact_api.req_add_contact(ncvd, auth_header)
    assert response_add.status_code == 201
    cont_id = response_add.json()["_id"]

    # Method PATCH (update contact)
    payload = EditData.updated_data
    response_upd = contact_api.req_patch_upd_contact(cont_id, payload, auth_header)
    assert response_upd.status_code == 200, f"Expected 200, got {response_upd.status_code}"

    # Checking body responce
    data_to_check = response_upd.json()
    assert "_id" in data_to_check
    assert "owner" in data_to_check
    assert "__v" in data_to_check
    assert data_to_check['firstName'] == payload['firstName']
    assert data_to_check['lastName'] == payload['lastName']
    assert data_to_check['birthdate'] == payload['birthdate']
    assert data_to_check['email'] == payload['email']
    assert data_to_check['phone'] == payload['phone']
    assert data_to_check['street1'] == payload['street1']
    assert data_to_check['street2'] == payload['street2']
    assert data_to_check['city'] == payload['city']
    assert data_to_check['stateProvince'] == payload['stateProvince']
    assert data_to_check['postalCode'] == payload['postalCode']
    assert data_to_check['country'] == payload['country']

    logger.success("Contact was successfully updated and response contains all required fields")
    # Finale clear
    try:
        contact_api.delete_contact(auth_header, cont_id)
    except Exception as e:
        logger.warning(f"Error message: {e}")


@pytest.mark.regression
@pytest.mark.api
def test_update_contact_with_invalid_contact_id():
    # Create contact
    contact_api = ContActsApi()
    auth_header = contact_api.auth_and_get_header(usr)
    response_add = contact_api.req_add_contact(ncvd, auth_header)
    assert response_add.status_code == 201
    cont_id = response_add.json()["_id"]
    cont_id_fake = "invalid_id"

    # Method PATCH (update contact)
    payload = EditData.updated_data
    response_upd = contact_api.req_patch_upd_contact(cont_id_fake, payload, auth_header)
    assert response_upd.status_code == 400, f"Expected 400, got {response_upd.status_code}"
    assert "Invalid Contact ID" in response_upd.text
    logger.success("The expected status code 400 has "
                   "been received with message 'Invalid Contact ID'")
    # Finale clear
    try:
        contact_api.delete_contact(auth_header, cont_id)
    except Exception as e:
        logger.warning(f"Error message: {e}")


@pytest.mark.regression
@pytest.mark.api
def test_update_contact_with_empty_data():
    # Create contact
    contact_api = ContActsApi()
    auth_header = contact_api.auth_and_get_header(usr)
    response_add = contact_api.req_add_contact(ncvd, auth_header)
    assert response_add.status_code == 201
    cont_id = response_add.json()["_id"]

    # Method PATCH (update contact)
    payload = EditData.updated_data_empty
    response_upd = contact_api.req_patch_upd_contact(cont_id, payload, auth_header)

    # Checking errors
    assert response_upd.status_code == 400, f"Expected 400, got {response_upd.status_code}"
    assert "`firstName` is required." in response_upd.text
    assert "`lastName` is required." in response_upd.text
    assert "Phone number is invalid" in response_upd.text
    logger.success(f"The expected status code 400 has been "
                   f"received with message: {response_upd.text}")
    # Finale clear
    try:
        contact_api.delete_contact(auth_header, cont_id)
    except Exception as e:
        logger.warning(f"Error message: {e}")


@pytest.mark.api
def test_update_deleted_contact():
    # Create contact
    contact_api = ContActsApi()
    auth_header = contact_api.auth_and_get_header(usr)
    response_add = contact_api.req_add_contact(ncvd, auth_header)
    assert response_add.status_code == 201
    cont_id = response_add.json()["_id"]

    # Delete contact
    delete_resp = contact_api.delete_contact(auth_header, cont_id)
    assert delete_resp.status_code == 200, f"Expected 200, got {delete_resp.status_code}"
    assert delete_resp.text.strip() == "Contact deleted"

    # Method PATCH (update contact)
    payload = EditData.updated_data
    response_upd = contact_api.req_patch_upd_contact(cont_id, payload, auth_header)
    assert response_upd.status_code == 404, f"Expected 404, got {response_upd.status_code}"

    logger.success("The expected status code 404 has been received "
                   "when trying to edit a deleted contact")


@pytest.mark.regression
@pytest.mark.api
def test_update_contact_with_invalid_data():
    # Create contact
    contact_api = ContActsApi()
    auth_header = contact_api.auth_and_get_header(usr)
    response_add = contact_api.req_add_contact(ncvd, auth_header)
    assert response_add.status_code == 201
    cont_id = response_add.json()["_id"]

    # Method PATCH (update contact)
    payload = EditData.updated_data_invalid
    response_upd = contact_api.req_patch_upd_contact(cont_id, payload, auth_header)
    assert response_upd.status_code == 400, f"Expected 400, got {response_upd.status_code}"

    # Checking errors
    assert "Birthdate is invalid" in response_upd.text
    assert "Email is invalid" in response_upd.text
    assert "is longer than the maximum allowed length (15)" in response_upd.text
    logger.success(f"The expected status code 400 has been "
                   f"received with message: {response_upd.text}")

    # Finale clear
    try:
        contact_api.delete_contact(auth_header, cont_id)
    except Exception as e:
        logger.warning(f"Error message: {e}")
