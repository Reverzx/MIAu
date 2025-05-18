import requests
from jsonschema import validate, ValidationError
from loguru import logger
from test_data.env import Env
from api_actions.catch_request_exception import catch_request_exception


class UserActsApi():

    def __init__(self):
        self.signup_url = f'{Env.URL_Login}users'
        self.usr_profile_url = f'{self.signup_url}/me'
        self.login_url = f'{self.signup_url}/login'
        self.header = {
            'Authorization': 'Bearer {{token}}'
            }

    def get_header(self, body):
        """
        Authorizates user, gets token
        Returns header with actual token
        """
        json = {
            'email': body['email'],
            'password': body['password']
        }
        auth = requests.post(url=self.login_url, json=json)
        token = auth.json()['token']
        header = {
            'Authorization': f'{token}'
        }
        return header

    @catch_request_exception
    def post_sign_up(self, body):
        """
        Sends a POST request with provided user credentials to register a new user
        """
        return requests.post(url=self.signup_url, headers=self.header, json=body)

    def is_response_schema_correct(self, response, expected_schema):
        """
        Checks if response JSON fits to expected schema.
        Returns True if response fits, otherwise False
        """
        current_schema = response.json()
        try:
            validate(current_schema, expected_schema)
            return True
        except ValidationError as v:
            logger.warning(f"JSON schema validation error: {v}")
            return False

    @catch_request_exception
    def patch_upd_user(self, body, upd_body):
        """
        Sends a PATCH request with provided user credentials to update user profile
        """
        head = self.get_header(body)
        return requests.patch(url=self.usr_profile_url, headers=head, json=upd_body)

    def upd_usr_with_invalid_data(self, body, upd_body):
        """
        Sends a PATCH request with provided data.
        Doesn't raise exceptions, is used to check the updating user profile with invalid data
        Returns the response object
        """
        head = self.get_header(body)
        return requests.patch(url=self.usr_profile_url, headers=head, json=upd_body)

    @catch_request_exception
    def get_user_profile(self, body):
        """
        Sends a GET request with provided data to get user's data
        Returns the response object
        """
        head = self.get_header(body)
        return requests.get(url=self.usr_profile_url, headers=head)

    @catch_request_exception
    def delete_user(self, header):
        """
        Removes user from database
        """
        return requests.delete(url=self.usr_profile_url, headers=header)
