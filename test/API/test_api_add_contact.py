import pytest
from loguru import logger
from pages.api_contact_actions import ContActsApi
from test_data.contacts_data import (
user_to_add_cont as usr,
new_cont_valid_data as ncvd,
new_cont_not_full as ncnf,
new_cont_empty_mand_fields as emf,
new_cont_invalid_data as ncid,
inv_phone as ip, inv_adress_data as iad
)


def test_add_contact_201():
    newcont = ContActsApi()
    response = newcont.add_cont_valid_data(usr, ncvd)
    assert response.status_code == 201
    logger.success('Response status code is 201')
    newcont.clear_cont_list(usr)


def test_response_body():
    newcont = ContActsApi()
    response = newcont.add_cont_valid_data(usr, ncvd)
    data_to_check = response.json()
    assert '_id' in data_to_check
    assert 'owner' in data_to_check
    assert '__v' in data_to_check
    assert data_to_check['firstName'] == ncvd['firstName']
    assert data_to_check['lastName'] == ncvd['lastName']
    assert data_to_check['birthdate'] == ncvd['birthdate']
    assert data_to_check['email'] == ncvd['email']
    assert data_to_check['phone'] == ncvd['phone']
    assert data_to_check['street1'] == ncvd['street1']
    assert data_to_check['street2'] == ncvd['street2']
    assert data_to_check['city'] == ncvd['city']
    assert data_to_check['stateProvince'] == ncvd['stateProvince']
    assert data_to_check['postalCode'] == ncvd['postalCode']
    assert data_to_check['country'] == ncvd['country']
    logger.success('Response body contains all the necessary details')
    newcont.clear_cont_list(usr)


def test_add_cont_response_schema():
    newcont = ContActsApi()
    assert newcont.is_response_schema_correct(usr, ncvd)
    logger.success("Correct response JSON schema")
    newcont.clear_cont_list(usr)


def test_is_new_cont_added():
    newcont = ContActsApi()
    assert newcont.get_cont_list_after_add_new_cont(usr, ncvd)
    logger.success('New contact was successfully added')
    newcont.clear_cont_list(usr)


def test_add_cont_filling_mand_fields():
    newcont = ContActsApi()
    response = newcont.add_cont_valid_data(usr, ncnf)
    assert response.status_code == 201
    logger.success('Response status code is 201')
    newcont.clear_cont_list(usr)


def test_not_full_data_schema():
    newcont = ContActsApi()
    assert newcont.is_response_schema_correct(usr, ncnf)
    logger.success("Correct response JSON schema")
    newcont.clear_cont_list(usr)


@pytest.mark.parametrize('body, description', emf)
def test_add_cont_empty_mand_fields(body, description):
    logger.info(f'Add contact with invalid credentials: {description}')
    newcont = ContActsApi()
    response = newcont.add_cont_invalid_data(usr, body)
    assert response.status_code == 400
    logger.success('Response status code is 400')


@pytest.mark.parametrize('body, description', ncid)
def test_add_cont_common_inv_data(body, description):
    logger.info(f'Add contact with invalid credentials: {description}')
    newcont = ContActsApi()
    response = newcont.add_cont_invalid_data(usr, body)
    assert response.status_code == 400
    logger.success('Response status code is 400')


@pytest.mark.parametrize('body, description', ip)
def test_add_cont_invalid_phone(body, description):
    logger.info(f'Add contact with invalid credentials: {description}')
    newcont = ContActsApi()
    response = newcont.add_cont_invalid_data(usr, body)
    assert response.status_code == 400
    logger.success(f"Response status code is 400. {response.json()['message']}")


@pytest.mark.xfail
@pytest.mark.parametrize('body, description', iad)
def test_add_cont_invalid_adress_data(body, description):
    logger.info(f'Add contact with invalid credentials: {description}')
    newcont = ContActsApi()
    response = newcont.add_cont_invalid_data(usr, body)
    assert response.status_code == 400
    logger.success("Response status code is 400")
