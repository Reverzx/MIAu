import requests
from test_data.env import Env
from loguru import logger


def post_login(email, password):
    url = f"{Env.URL_Login}users/login"
    body = {
        "email": email,
        "password": password
    }
    response = None
    try:
        response = requests.post(url, json=body)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        logger.warning(f"HTTP error occurred: {e}")
        return response
    except requests.exceptions.RequestException as e:
        logger.warning(f"Request error occurred: {e}")
        return None
