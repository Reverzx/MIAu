import requests
from loguru import logger
from test_data.env import Env
from api_actions.api_user_actions import UserActsApi
from api_actions.catch_request_exception import catch_request_exception


class ContActsApi():
    def __init__(self):
        self.url = f'{Env.URL_Login}contacts'

    def auth_and_get_header(self, user_body):
        """
        Authorizates user, gets token
        Returns header with actual token
        """
        req = UserActsApi()
        header = req.get_header(user_body)
        return header

    def req_add_contact(self, cont_data, header):
        """
        Sends POST request With provided data to add new contact
        """
        return requests.post(url=self.url, headers=header, json=cont_data)

    def req_get_contact_list(self, header):
        """
        Sends GET request to get contact list of definded user
        """
        return requests.get(url=self.url, headers=header)

    def req_get_contact(self, cont_id, header):
        """
        Sends GET request to get data of definded contact, using contact's ID
        """
        return requests.get(url=f'{self.url}/{cont_id}', headers=header)

    def req_put_upd_contact(self, cont_id, upd_data, header):
        """
        Sends PUT request with provided data to update contact data.
        Requires to use all the fields. Uses contact's ID
        """
        return requests.put(url=f'{self.url}/{cont_id}', headers=header, json=upd_data)

    def req_patch_upd_contact(self, cont_id, upd_data, header):
        """
        Sends PATCH request with provided data to partly update contact data.
        Permits to use only chosen fields. Uses contact's ID
        """
        return requests.patch(url=f'{self.url}/{cont_id}', headers=header, json=upd_data)

    def delete_contact(self, header, cont_id):
        """
        Sends DELETE request to remove defined contact from contact list
        Uses contact's ID
        """
        return requests.delete(url=f'{self.url}/{cont_id}', headers=header)

    @catch_request_exception
    def add_contact(self, user_body, new_cont):
        """
        Authorizes a user and adds a new contact with provided data
        """
        header = self.auth_and_get_header(user_body)
        return self.req_add_contact(new_cont, header)

    def is_response_schema_correct(self, response, expected_schema):
        """
        Checks if response JSON fits to expected schema.
        Returns True if response fits, otherwise False
        """
        check = UserActsApi()
        return check.is_response_schema_correct(response, expected_schema)

    def clear_cont_list(self, user):
        """
        Removes all records from user's profile
        """
        header = self.auth_and_get_header(user)
        cont_list = self.req_get_contact_list(header).json()
        ids = []
        for item in cont_list:
            ids.append(item['_id'])
        for item in ids:
            self.delete_contact(header, item)

    def add_contact_and_check_is_added(self, user, new_cont):
        """
        Adds new contact with provided data to contact list, gets new contact's ID
        After addition collects all IDs in contact list, checks if new contact's ID
        is in IDs list.
        """
        header = self.auth_and_get_header(user)
        addition = self.req_add_contact(new_cont, header)
        cont_id = addition.json()['_id']
        response = self.req_get_contact_list(header)
        if not response:
            logger.warning("No response returned")
            return False
        ids = []
        for item in response.json():
            ids.append(item['_id'])
        if cont_id in ids:
            logger.success('New contact was successfully added to contact list')
            return True
        else:
            logger.warning('The new contact was not added to contact list')
            return False
