from loguru import logger
from test_data.env import Env
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from pages.add_contact_page import AddContactPage
from pages.contact_details_page import ContactDetailsPage
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementClickInterceptedException)


class ContactListPage(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.add_contact_button = (By.ID, 'add-contact')
        self.contact_row = (By.XPATH, '//tr[@class="contactTableBodyRow"]')
        self.logout_button = (By.ID, 'logout')

    def is_contact_list_page(self):
        return self.is_url_correct(Env.URL_ContactList)

    def navigate_to_add_contact_page(self):
        self.click_button(self.add_contact_button)
        return AddContactPage(self.driver, self.url)

    def navigate_to_contact_details_page(self):
        try:
            self.click_button(self.contact_row)
            return ContactDetailsPage(self.driver, self.url)
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            logger.error(f"Not found the contact details page: {e}")
            return None

    def logout(self):
        self.click_button(self.logout_button)
