from loguru import logger
from api_actions.api_contact_actions import ContActsApi
from test_data.edit_data import EditData
from test_data.contacts_data import user_to_add_contact as usr, new_contact_valid_data as ncvd


def test_successful_contact_deletion():
    contact_api = ContActsApi()
    auth_header = contact_api.auth_and_get_header(usr)
    cont_id = contact_api.req_add_contact(ncvd, auth_header).json()["_id"]
    delete_resp = contact_api.delete_contact(auth_header, cont_id)
    assert delete_resp.status_code == 200, f"Expected 200, got {delete_resp.status_code}"
    assert delete_resp.text.strip() == "Contact deleted"
    logger.success('Contact deleted successfully')


def test_delete_contact_already_deleted():
    contact_api = ContActsApi()
    auth_header = contact_api.auth_and_get_header(usr)
    cont_id = contact_api.req_add_contact(ncvd, auth_header).json()["_id"]
    delete_resp = contact_api.delete_contact(auth_header, cont_id)
    assert delete_resp.status_code == 200, f"Expected 200, got {delete_resp.status_code}"
    delete_already_resp = contact_api.delete_contact(auth_header, cont_id)
    assert delete_already_resp.status_code == 404, (f"Expected 404, got "
                                                    f"{delete_already_resp.status_code}")
    logger.success('The expected status code 404 has been received')


def test_delete_contact_with_invalid_id():
    contact_api = ContActsApi()
    auth_header = contact_api.auth_and_get_header(usr)
    delete_resp = contact_api.delete_contact(auth_header, 'invalid_cont_id')
    assert delete_resp.status_code == 400
    logger.success('The expected status code 400 has been received')


def test_try_update_deleted_contact():
    contact_api = ContActsApi()
    auth_header = contact_api.auth_and_get_header(usr)
    response_add = contact_api.req_add_contact(ncvd, auth_header)
    cont_id = response_add.json()["_id"]
    delete_resp = contact_api.delete_contact(auth_header, cont_id)
    assert delete_resp.status_code == 200, f"Expected 200, got {delete_resp.status_code}"
    payload = EditData.updated_data
    response = contact_api.req_put_upd_contact(cont_id, payload, auth_header)
    assert response.status_code == 404
    logger.success('The expected status code 404 has been received')
