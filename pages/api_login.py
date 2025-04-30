import requests
from jsonschema.exceptions import ValidationError
from test_data.env import Env
from jsonschema import validate
from loguru import logger


class LoginAPI:
    def __init__(self):
        self.url = Env.URL_Login
        self.endpoint = '/users/login'
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
                    "required": ["_id", "firstName", "lastName",
                                 "email", "__v"]
                },
                "token": {"type": "string"}
            },
            "required": ["user", "token"]
        }

    def post_login(self, email, password):
        body = {
            "email": email,
            "password": password
        }
        response = None
        try:
            response = requests.post(f'{self.url}{self.endpoint}', json=body)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            logger.warning(f"HTTP error occurred: {e}")
            return response
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request error occurred: {e}")
            return None

    def is_response_schema_correct(self, email, password):
        response = self.post_login(email, password)
        if not response:
            logger.warning("No response returned from login")
            return False
        try:
            current_schema = response.json()
            validate(current_schema, self.schema)
            return True
        except ValidationError as e:
            logger.warning(f"JSON schema validation error: {e}")
            return False

    def post_login_with_missing_email_parameter(self, password):
        body = {
            "password": password
        }
        return requests.post(f'{self.url}{self.endpoint}', json=body)

    def post_login_with_missing_password_parameter(self, email):
        body = {
            "email": email
        }
        return requests.post(f'{self.url}{self.endpoint}', json=body)
