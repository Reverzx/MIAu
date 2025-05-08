from pages.add_contact_page import AddContactPage
from pages.contact_details_page import ContactDetailsPage
from test_data.env import Env
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementClickInterceptedException)


class ContactListPage(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.add_contact_button = (By.ID, 'add-contact')
        self.contact_row = (By.XPATH, '//tr[@class="contactTableBodyRow"]')

    def is_contact_list_page(self):
        """
        Checks whether the current URL matches the Contact List page URL.
        :return: True if the current URL is correct, otherwise False.
        """
        return self.is_url_correct(Env.URL_ContactList)

    def navigate_to_add_contact_page(self):
        """
        Clicks the Add Contact button and navigates to the Add Contact page.
        :return: AddContactPage object
        """
        self.click_button(self.add_contact_button)
        return AddContactPage(self.driver, self.url)

    def is_navigate_to_add_contact_page_successful(self):
        """
        Waits up to 5 seconds for a successful redirect to the Add Contact page.
        :return: bool: True if the current URL matches the Add Contact page url,
        otherwise False.
        """
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(Env.URL_AddContact)
        )
        return True

    def navigate_to_contact_details_page(self):
        """
        Clicks the first contact row to navigate to the Contact Details page.
        :return: ContactDetailsPage object
        """
        try:
            self.click_button(self.contact_row)
            return ContactDetailsPage(self.driver, self.url)
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            logger.error(f"Not found the contact details page: {e}")
            return None

    def is_navigate_to_contact_details_page_successful(self):
        """
        Waits up to 5 seconds for a successful redirect to the Contact Details page.
        :return: bool: True if the current URL matches the Contact Details page url,
        otherwise False.
        """
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(Env.URL_ContactDetails)
        )
        return True
