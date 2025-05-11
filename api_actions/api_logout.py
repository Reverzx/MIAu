import requests
from test_data.env import Env
from loguru import logger


def post_logout(auth_token):
    url = f"{Env.URL_Login}/users/logout"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = None
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        logger.warning(f"HTTP error occurred: {e}")
        return response
    except requests.exceptions.RequestException as e:
        logger.warning(f"Request error occurred: {e}")
        return None


def assert_unauthorized_request(response):
    """
    Verifies that the response status code is 401 Unauthorized
    and the error message is "Please authenticate."
    """
    assert response.status_code == 401,\
        f"Wrong status code: {response.status_code}. Expected: 401"
    assert response.json().get("error") == "Please authenticate.", \
        (f"Missing or wrong error message in the response json: {response.json()}. "
         f"Expected: {'Please authenticate.'}")
