import requests
from test_data.env import Env


def add_contact_and_get_id(token, payload):
    url = f"{Env.URL_Login}contacts/"
    headers = {"Authorization": f"Bearer {token}"}
    add_cont = requests.post(url, headers=headers, json=payload)
    return add_cont.json()["_id"]
