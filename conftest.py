# pylint: disable=redefined-outer-name
import sys
import json
import tempfile
from pathlib import Path
import pytest
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from api_actions.api_user_actions import UserActsApi
from api_actions.api_contact_actions import ContActsApi
from test_data.register_data import user_to_add, usr_to_delete
from test_data.usr_update_data import user_to_be_update, upd_data
from test_data.contacts_data import user_to_add_contact
from test_data.user_creds import UserCredentials
from test_data.env import Env
from test_data.edit_data import EditData
from pages.login_page import LoginPage
from pages.contact_details_page import ContactDetailsPage


def pytest_configure(config):  # pylint: disable=unused-argument
    logger.remove()
    logger.add(sys.stdout, level='INFO')


@pytest.fixture
def driver():
    logger.info("Launching headless-browser")
    _options = webdriver.ChromeOptions()
    _options.add_argument("--headless")

    # Added to resolve CI and Jenkins issues
    # Start
    _options.add_argument("--no-sandbox")
    _options.add_argument("--disable-dev-shm-usage")
    _options.add_argument("--disable-gpu")
    _options.add_argument("--disable-extensions")
    _options.add_argument("--window-size=1920,1080")

    user_data_dir = tempfile.mkdtemp()
    _options.add_argument(f"--user-data-dir={user_data_dir}")
    # End

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    _options.add_experimental_option("prefs", prefs)
    _options.add_argument("--incognito")
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=_options
    )
    browser.implicitly_wait(5)
    yield browser
    logger.info("Closing browser")
    browser.quit()


@pytest.fixture
def read_schema():
    path = Path(__file__).parents[0] / "test_data" / "response_schemas.json"
    with path.open() as f:
        return json.load(f)


@pytest.fixture(scope='function')
def delete_user(request):
    """
    Deletes added user after test's run. Used in test Add User
    """
    def fin():
        delete = UserActsApi()
        delete.delete_user(user_to_add)
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


@pytest.fixture()
def login_page(driver):
    login = LoginPage(driver, Env.URL_Login)
    login.open()
    return login


@pytest.fixture()
def create_contact_and_locate_edit_page(driver):
    """
    The fixture is used for edit contact page testing.
    Created with specified credentials: it_edit_email, it_edit_password.
    """
    # Navigate to Login page
    login = LoginPage(driver, Env.URL_Login)
    login.open()

    # Navigate to Contact List page
    contact_list = login.complete_login(
        UserCredentials.it_edit_email,
        UserCredentials.it_edit_password
    )
    logger.info("The user is logged in and redirected to the Contact List page")

    # Navigate to Add Contact page
    add_contact = contact_list.navigate_to_add_contact_page()

    # Add a new contact
    add_contact.fill_contact_form(EditData.contact_data_only_mandatory)
    add_contact.submit()
    logger.info("A new contact is added.")

    # Navigate to Contact Details page
    contact_details = contact_list.navigate_to_contact_details_page()

    # Navigate to Edit Contact page
    edit_page = contact_details.navigate_to_edit_contact_page()

    return edit_page


@pytest.fixture
def delete_contact(driver):
    yield
    contact_details_page = ContactDetailsPage(driver, Env.URL_ContactDetails)
    contact_details_page.delete_contact()
    logger.info("The contact is deleted via fixture after test.")
