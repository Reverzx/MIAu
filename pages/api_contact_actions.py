import requests
from jsonschema import validate
from loguru import logger
from test_data.env import Env
from jsonschema import ValidationError
from pages.api_user_actions import UserActsApi


class ContActsApi():
    def __init__(self):
        self.url = f'{Env.URL_Login}contacts'
        self.schema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "_id": {"type": "string"},
                "firstName": {"type": "string"},
                "lastName": {"type": "string"},
                "birthdate": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
                "street1": {"type": "string"},
                "street2": {"type": "string"},
                "city": {"type": "string"},
                "stateProvince": {"type": "string"},
                "postalCode": {"type": "string"},
                "country": {"type": "string"},
                "owner": {"type": "string"},
                "__v": {"type": "integer"}
            },
            "required": ["_id", "firstName", "lastName", "owner", "__v"]
        }

    def auth_and_get_token(self, usr_body):
        req = UserActsApi()
        header = req.authorizate_and_get_token(usr_body)
        return header

    def add_contact(self, cont_data, header):
        response = None
        try:
            response = requests.post(url=self.url, headers=header, json=cont_data)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h:
            logger.warning(f'HTTP error occured: {h}')
            return response
        except requests.exceptions.RequestException as r:
            logger.warning(f'Request error occured: {r}')
            return None

    def get_contact_list(self, header):
        response = None
        try:
            response = requests.get(url=self.url, headers=header)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h:
            logger.warning(f'HTTP error occured: {h}')
            return response
        except requests.exceptions.RequestException as r:
            logger.warning(f'Request error occured: {r}')
            return None

    def get_contact(self, cont_id, header):
        response = None
        try:
            response = requests.get(url=f'{self.url}/{cont_id}', headers=header)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h:
            logger.warning(f'HTTP error occured: {h}')
            return response
        except requests.exceptions.RequestException as r:
            logger.warning(f'Request error occured: {r}')
            return None

    def put_upd_contact(self, cont_id, upd_data, header):
        response = None
        try:
            response = requests.put(url=f'{self.url}/{cont_id}', headers=header, json=upd_data)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h:
            logger.warning(f'HTTP error occured: {h}')
            return response
        except requests.exceptions.RequestException as r:
            logger.warning(f'Request error occured: {r}')
            return None

    def patch_upd_contact(self, cont_id, upd_data, header):
        response = None
        try:
            response = requests.patch(url=f'{self.url}/{cont_id}', headers=header, json=upd_data)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h:
            logger.warning(f'HTTP error occured: {h}')
            return response
        except requests.exceptions.RequestException as r:
            logger.warning(f'Request error occured: {r}')
            return None

    def delete_contact(self, header, cont_id):
        response = None
        try:
            response = requests.patch(url=f'{self.url}/{cont_id}', headers=header)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h:
            logger.warning(f'HTTP error occured: {h}')
            return response
        except requests.exceptions.RequestException as r:
            logger.warning(f'Request error occured: {r}')
            return None
