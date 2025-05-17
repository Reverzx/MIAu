import pytest
from api_actions.api_contact_actions import UserActsApi
from api_actions.api_contact_actions import ContActsApi
from test_data.register_data import usr_to_add, usr_to_delete
from test_data.usr_update_data import user_to_be_update, upd_data
from test_data.contacts_data import user_to_add_contact


@pytest.fixture(scope='function')
def delete_user(request):
    """
    Deletes added user after test's run. Used in test Add User
    """
    def fin():
        delete = UserActsApi()
        delete.delete_user(usr_to_add)
    request.addfinalizer(fin)


@pytest.fixture(scope='function')
def sign_up_user(request):
    """
    Adds deleted user after test's run. Used in test Delete User
    """
    def fin():
        signup = UserActsApi()
        signup.post_sign_up(usr_to_delete)
    request.addfinalizer(fin)


@pytest.fixture(scope='function')
def revert_updation(request):
    """
    Made updated user's data back after test's run. Used in test Update user
    """
    def fin():
        revert = UserActsApi()
        revert.patch_upd_user(upd_data, user_to_be_update)
    request.addfinalizer(fin)


@pytest.fixture(scope='function')
def clear_contacts(request):
    """
    Clears contact list after test's run. Used in test Add contact
    """
    def fin():
        clear = ContActsApi()
        clear.clear_cont_list(user_to_add_contact)
    request.addfinalizer(fin)
