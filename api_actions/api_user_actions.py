import requests
from jsonschema import validate, ValidationError
from loguru import logger
from test_data.env import Env


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
        Returns token
        """
        json ={
            'email': body['email'],
            'password': body['password']
        }
        auth = requests.post(url=self.login_url, json=json)
        token = auth.json()['token']
        header = {
            'Authorization': f'{token}'
        }
        return header

    def post_sign_up(self, body):
        """
        Sends a POST request with provided user credentials
        Returns the response if the request has been made, in case od exception - None
        """
        response = None
        try:
            response = requests.post(url=self.signup_url, headers=self.header, json=body)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as h:
            logger.warning(f'HTTP error occured: {h}')
            return response
        except requests.exceptions.RequestException as r:
            logger.warning(f'Request error occured: {r}')
            return None

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


    def patch_upd_user(self, body, upd_body):
        """
        Sends a PATCH request with provided user credentials to update user profile
        Returns the response if the request has been made, in case od exception - None
        """
        response = None
        head = self.get_header(body)
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
        head = self.get_header(body)
        return requests.patch(url=self.usr_profile_url, headers=head, json=upd_body)

    def sign_up_with_invalid_data(self, body):
        """
        Sends a POST request with provided data.
        Doesn't raise exceptions, is used to check the signing up with invalid data
        Returns the response object
        """
        return requests.post(url=self.signup_url, headers=self.header, json=body)

    def get_user_profile(self, body):
        """
        Sends a GET request with provided data to get user's data
        Returns the response object
        """
        head = self.get_header(body)
        response = requests.get(url=self.usr_profile_url, headers=head)
        return response

    def delete_user(self, body):
        """
        Removes user from database
        """
        head = self.get_header(body)
        return requests.delete(url=self.usr_profile_url, headers=head)

    def double_delete_user(self, body):
        """
        Removes user from database, than repeats the deletion
        """
        del_url = self.usr_profile_url
        head = self.get_header(body)
        requests.delete(url=del_url, headers=head)
        return requests.delete(url=del_url, headers=head)

    def get_deleted_user(self, body):
        """
        Removes user from database, than tries to get user's data
        """
        head = self.get_header(body)
        requests.delete(url=self.usr_profile_url, headers=head)
        return requests.get(url=self.usr_profile_url, headers=head)
