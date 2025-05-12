import requests
from test_data.env import Env


def put_contact_upd(token, cont_id, payload):
    url = f"{Env.URL_Login}contacts/{cont_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.put(url, headers=headers, json=payload)
