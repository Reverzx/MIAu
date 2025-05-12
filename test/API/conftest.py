from pathlib import Path
import json
import pytest
from api_actions.api_contact_actions import ContActsApi
from test_data.contacts_data import user_to_add_cont as usr, new_cont_valid_data as ncvd


@pytest.fixture
def read_schema():
    path = Path(__file__).parents[2] / "test_data" / "response_schemas.json"
    with path.open() as f:
        return json.load(f)

@pytest.fixture
def auth_header():
    contact_api = ContActsApi()
    return contact_api.auth_and_get_token(usr)

@pytest.fixture
def contact_setup(auth_header):
    contact_api = ContActsApi()
    response_add = contact_api.req_add_contact(ncvd, auth_header)
    assert response_add.status_code == 201
    cont_id = response_add.json()["_id"]
    yield auth_header, cont_id
    try:
        contact_api.delete_contact(auth_header, cont_id)
    except Exception:
        pass
