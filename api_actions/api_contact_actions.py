import requests
from jsonschema import validate, ValidationError
from loguru import logger
from test_data.env import Env
from api_actions.api_user_actions import UserActsApi


class ContActsApi():
    def __init__(self):
        self.url = f'{Env.URL_Login}contacts'

    def auth_and_get_header(self, usr_body):
        req = UserActsApi()
        header = req.get_header(usr_body)
        return header

    def req_add_contact(self, cont_data, header):
        return requests.post(url=self.url, headers=header, json=cont_data)

    def req_get_contact_list(self, header):
        return requests.get(url=self.url, headers=header)

    def req_get_contact(self, cont_id, header):
        return requests.get(url=f'{self.url}/{cont_id}', headers=header)

    def req_put_upd_contact(self, cont_id, upd_data, header):
        return requests.put(url=f'{self.url}/{cont_id}', headers=header, json=upd_data)

    def req_patch_upd_contact(self, cont_id, upd_data, header):
        return requests.patch(url=f'{self.url}/{cont_id}', headers=header, json=upd_data)

    def delete_contact(self, header, cont_id):
        return requests.delete(url=f'{self.url}/{cont_id}', headers=header)

    def add_cont_valid_data(self, user, new_cont):
        header = self.auth_and_get_header(user)
        response = None
        try:
            response = self.req_add_contact(new_cont, header)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h:
            logger.warning(f'HTTP error occured: {h}')
            return response
        except requests.exceptions.RequestException as r:
            logger.warning(f'Request error occured: {r}')
            return None

    def add_cont_invalid_data(self, user, new_cont):
        header = self.auth_and_get_header(user)
        return self.req_add_contact(new_cont, header)

    def is_response_schema_correct(self, user, new_cont):
        header = self.auth_and_get_header(user)
        response = self.req_add_contact(new_cont, header)
        if not response:
            logger.warning("No response returned")
            return False
        try:
            current_schema = response.json()
            validate(current_schema, self.schema)
            return True
        except ValidationError as v:
            logger.warning(f"JSON schema validation error: {v}")
            return False

    def clear_cont_list(self, user):
        header = self.auth_and_get_header(user)
        cont_list = self.req_get_contact_list(header).json()
        ids = []
        for item in cont_list:
            ids.append(item['_id'])
        for item in ids:
            self.delete_contact(header, item)

    def get_cont_list_after_add_new_cont(self, user, new_cont):
        header = self.auth_and_get_header(user)
        addition = self.req_add_contact(new_cont, header)
        cont_id = addition.json()['_id']
        response = self.req_get_contact_list(header)
        if not response:
            logger.warning("No response returned")
            return False
        ids = []
        for item in response.json():
            ids.append(item['_id'])
        if cont_id in ids:
            return True
        else:
            logger.warning('The new contact was not added to contact list')
            return False
