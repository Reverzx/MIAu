import requests
from jsonschema import validate
from loguru import logger
from test_data.env import Env
from jsonschema import ValidationError


class UserActsApi():

    def __init__(self):
        self.url = Env.url_add_user_api
        self.header = {
            'Authorization': 'Bearer {{token}}'
            }
        self.schema = {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "_id": {"type": "string"},
                        "firstName": {"type": "string"},
                        "lastName": {"type": "string"},
                        "email": {"type": "string"},
                        "__v": {"type": "number"}
                    },
                    "required": ["_id", "firstName", "lastName", "email", "__v"]
                },
                "token": {"type": "string"}
            },
            "required": ["user", "token"]
        }

    def post_sign_up(self, body):
        """
        Sends a POST request with provided user credentials
        Returns the response if the request has been made, in case od exception - None
        """
        response = None
        try:
            response = requests.post(url=self.url, headers=self.header, json=body)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h:
            logger.warning(f'HTTP error occured: {h}')
            return response
        except requests.exceptions.RequestException as r:
            logger.warning(f'Request error occured: {r}')
            return None

    def is_response_schema_correct(self, body):
        """
        Sends a POST request with provided user credentials, checks if response JSON
        fits to expected schema.
        Returns True if response fits, otherwise False
        """
        response = self.post_sign_up(body)
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

    def sign_up_with_invalid_data(self, body):
        """
        Sends a POST request with provided data.
        Doesn't raise exceptions, is used to check the signing up with invalid data
        Returns the response object
        """
        return requests.post(self.url, self.header, json=body)

    def get_user_profile(self, body):
        from pages.api_login import LoginAPI
        login = LoginAPI()
        get_url = Env.url_usr_details_api
        email = body['email']
        password = body['password']
        auth = login.post_login(email, password)
        token = auth.json()['token']
        head = {
            'Authorization': f'{token}'
        }
        response = requests.get(url=get_url, headers=head)
        return response

    def delete_user(self, body):
        """
        Removes user from database
        """
        from pages.api_login import LoginAPI
        login = LoginAPI()
        del_url = Env.url_usr_details_api
        email = body['email'],
        password = body['password']
        auth = login.post_login(email, password)
        token = auth.json()['token']
        head = {
            'Authorization': f'{token}'
        }
        return requests.delete(url=del_url, headers=head)

    def double_delete_user(self, body):
        """
        Removes user from database, than repeats the deletion
        """
        from pages.api_login import LoginAPI
        login = LoginAPI()
        del_url = Env.url_usr_details_api
        email = body['email'],
        password = body['password']
        auth = login.post_login(email, password)
        token = auth.json()['token']
        head = {
            'Authorization': f'{token}'
        }
        requests.delete(url=del_url, headers=head)
        return requests.delete(url=del_url, headers=head)

    def get_deleted_user(self, body):
        from pages.api_login import LoginAPI
        login = LoginAPI()
        url = Env.url_usr_details_api
        email = body['email'],
        password = body['password']
        auth = login.post_login(email, password)
        token = auth.json()['token']
        head = {
            'Authorization': f'{token}'
        }
        requests.delete(url=url, headers=head)
        return requests.get(url=url, headers=head)
