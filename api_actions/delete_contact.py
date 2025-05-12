import requests
from test_data.env import Env


def delete_contact(token, cont_id):
    url = f"{Env.URL_Login}contacts/{cont_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200, \
        f"Wrong status code: {response.status_code}. Expected: 200"
