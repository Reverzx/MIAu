import requests
from test_data.env import Env
from test_data.edit_data import EditData


def put_contact_upd(token, cont_id, payload):
    url = f"{Env.URL_Login}contacts/{cont_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.put(url, headers=headers, json=payload)
