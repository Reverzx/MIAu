import requests
from test_data.env import Env


def login_and_get_token(email, password):
    url = f"{Env.URL_Login}users/login"
    payload = {
            "email": email,
            "password": password
    }
    response = requests.post(url, json=payload)
    return response.json()["token"]
