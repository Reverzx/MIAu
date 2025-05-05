from pages.base_page import BasePage
from test_data.env import Env
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

    def is_add_contact_page(self):
        """
        Checks whether the current URL matches the Add Contact page URL.
        :return: True if the current URL is correct, otherwise False.
        """
        return self.is_url_correct(Env.URL_AddContact)

    def fill_contact_form(self, data):
        """
        Fills in the Add Contact form fields using the provided data.
        :param data: Dictionary of field IDs and values to fill.
        :raises ValueError: If a given field is not recognized.
        """
        for field_id, value in data.items():
            locator = self.elements.get(field_id)
            if locator:
                self.input_text(locator, value)
            else:
                raise ValueError(f"Unknown field: {field_id}")

    def submit(self):
        """
        Clicks the Submit button to attempt to save the new contact.
        """
        self.click_button(self.elements['submit'])
