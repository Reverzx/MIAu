import requests
from jsonschema import validate, ValidationError
from loguru import logger
from test_data.env import Env


class UserActsApi():

    def __init__(self):
        self.url = f'{Env.URL_Login}users'
        self.usr_profile_url = f'{Env.URL_Login}users/me'
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
        self.upd_schema = {
            "type": "object",
            "properties": {
                "_id": {"type": "string"},
                "firstName": {"type": "string"},
                "lastName": {"type": "string"},
                "email": {"type": "string"},
                "__v": {"type": "number"}
            },
            "required": ["_id", "firstName", "lastName", "email", "__v"]
        }

    def authorizate_and_get_token(self, body):
        """
        Authorizates user, gets token
        Returns token
        """
        from pages.api_login import LoginAPI
        login = LoginAPI()
        email = body['email'],
        password = body['password']
        auth = login.post_login(email, password)
        token = auth.json()['token']
        head = {
            'Authorization': f'{token}'
        }
        return head

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

    def is_response_update_schema_correct(self, body, upd_body):
        """
        Sends a PATCH request with provided user credentials, checks if response JSON
        fits to expected schema.
        Returns True if response fits, otherwise False
        """
        response = self.patch_upd_user(body, upd_body)
        if not response:
            logger.warning("No response returned")
            return False
        try:
            current_schema = response.json()
            validate(current_schema, self.upd_schema)
            return True
        except ValidationError as v:
            logger.warning(f"JSON schema validation error: {v}")
            return False

    def patch_upd_user(self, body, upd_body):
        """
        Sends a PATCH request with provided user credentials to update user profile
        Returns the response if the request has been made, in case od exception - None
        """
        response = None
        head = self.authorizate_and_get_token(body)
        try:
            response = requests.patch(url=self.usr_profile_url, headers=head, json=upd_body)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h:
            logger.warning(f'HTTP error occured: {h}')
            return response
        except requests.exceptions.RequestException as r:
            logger.warning(f'Request error occured: {r}')
            return None

    def upd_usr_with_invalid_data(self, body, upd_body):
        """
        Sends a PATCH request with provided data.
        Doesn't raise exceptions, is used to check the updating user profile with invalid data
        Returns the response object
        """
        head = self.authorizate_and_get_token(body)
        return requests.patch(url=self.usr_profile_url, headers=head, json=upd_body)

    def sign_up_with_invalid_data(self, body):
        """
        Sends a POST request with provided data.
        Doesn't raise exceptions, is used to check the signing up with invalid data
        Returns the response object
        """
        return requests.post(url=self.url, headers=self.header, json=body)

    def get_user_profile(self, body):
        """
        Sends a GET request with provided data to get user's data
        Returns the response object
        """
        head = self.authorizate_and_get_token(body)
        response = requests.get(url=self.usr_profile_url, headers=head)
        return response

    def delete_user(self, body):
        """
        Removes user from database
        """
        head = self.authorizate_and_get_token(body)
        return requests.delete(url=self.usr_profile_url, headers=head)

    def double_delete_user(self, body):
        """
        Removes user from database, than repeats the deletion
        """
        del_url = f'{self.url}/me'
        head = self.authorizate_and_get_token(body)
        requests.delete(url=del_url, headers=head)
        return requests.delete(url=del_url, headers=head)

    def get_deleted_user(self, body):
        """
        Removes user from database, than tries to get user's data
        """
        head = self.authorizate_and_get_token(body)
        requests.delete(url=self.usr_profile_url, headers=head)
        return requests.get(url=self.usr_profile_url, headers=head)
