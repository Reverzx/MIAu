from pages.add_contact_page import AddContactPage
from test_data.env import Env
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ContactDetailsPage(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.edit_contact_button = (By.XPATH, '//button[@id="edit-contact"]')

    def navigate_to_edit_contact_page(self):
        self.click_button(self.edit_contact_button)
        return AddContactPage(self.driver, self.url)

    def is_navigate_to_edit_contact_page_successful(self):
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(Env.URL_EditContact)
        )
        return True
