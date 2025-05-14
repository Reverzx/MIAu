from loguru import logger
from test_data.env import Env
from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class AddContactPage(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)

        self.elements = {
            'title': (By.TAG_NAME, 'h1'),
            'firstName': (By.ID, 'firstName'),
            'lastName': (By.ID, 'lastName'),
            'birthdate': (By.ID, 'birthdate'),
            'email': (By.ID, 'email'),
            'phone': (By.ID, 'phone'),
            'street1': (By.ID, 'street1'),
            'street2': (By.ID, 'street2'),
            'city': (By.ID, 'city'),
            'stateProvince': (By.ID, 'stateProvince'),
            'postalCode': (By.ID, 'postalCode'),
            'country': (By.ID, 'country'),
            'submit': (By.ID, 'submit'),
            'cancel': (By.ID, 'cancel'),
            'logout': (By.ID, 'logout'),
        }
        self.logout_button = (By.ID, 'logout')

    def navigate_to_add_contact_page(self, email, password):
        # Navigate to Login page
        from pages.login_page import LoginPage
        login_page = LoginPage(self.driver, Env.URL_Login)
        login_page.open()

        # Navigate to Contact List page
        contact_list = login_page.complete_login(email, password)
        logger.info("The user is logged in and redirected to the Contact List page")

        # Navigate to Add Contact page
        return contact_list.navigate_to_add_contact_page()

    def is_add_contact_page(self):
        return self.is_url_correct(Env.URL_AddContact)

    def fill_contact_form(self, data):
        for field_id, value in data.items():
            locator = self.elements.get(field_id)
            if locator:
                self.input_text(locator, value)
            else:
                raise ValueError(f"Unknown field: {field_id}")

    def submit(self):
        self.click_button(self.elements['submit'])

    def logout(self):
        self.click_button(self.logout_button)
