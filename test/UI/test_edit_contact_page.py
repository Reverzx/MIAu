import pytest
from loguru import logger
from test_data.env import Env
from pages.login_page import LoginPage
from test_data.user_creds import UserCredentials
from test_data.login_data import invalid_login_data_ui


def test_expected_elements_present(driver):
    assert is_element_present