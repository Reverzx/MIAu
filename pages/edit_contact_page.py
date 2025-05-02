import pytest
from loguru import logger
from pages.base_page import BasePage
from pages.login_page import LoginPage
from test_data.user_creds import UserCredentials
from test_data.env import Env
from selenium.webdriver.common.by import By


class EditContactPage(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)

    def is_edit_contact_page(self):
        """
        Checks whether the current URL matches the edit contact page URL.
        :return: bool: True if the current URL is correct, otherwise False.
        """
        return self.is_url_correct(Env.URL_EditContact)
