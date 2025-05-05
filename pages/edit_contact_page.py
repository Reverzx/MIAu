from pages.base_page import BasePage
from test_data.env import Env
from test_data.edit_data import EditData
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class EditContactPage(BasePage):
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
        self.error = (By.ID, 'error')

    def is_edit_contact_page(self):
        """
        Checks whether the current URL matches the Edit Contact page URL.
        :return: True if the current URL is correct, otherwise False.
        """
        return self.is_url_correct(Env.URL_EditContact)

    def edit_contact_form(self, data):
        """
        Fills in the Edit Contact form fields with the provided data.
        :param data: Dictionary of form fields and values to fill.
        :raises ValueError: If a given field is not recognized.
        """
        for field_id, value in data.items():
            locator = self.elements.get(field_id)
            if locator:
                self.input_text(locator, value)
            else:
                raise ValueError(f"Unknown field: {field_id}")

    def fill_fields_with_max_length_allowed(self):
        """
        Fills in the Edit Contact form fields using
        the maximum allowed number of characters for each field.
        :raises ValueError: If locator or corresponding test data is missing.
        """
        mapping = {
            'firstName': '20 chars',
            'lastName': '20 chars',
            'phone': '15 chars',
            'street1': '40 chars',
            'street2': '40 chars',
            'city': '40 chars',
            'stateProvince': '20 chars',
            'postalCode': '10 chars',
            'country': '40 chars'
        }
        for field_id, max_chars in mapping.items():
            locator = self.elements.get(field_id)
            text = EditData.max_length_allowed.get(max_chars)
            if locator and text:
                self.input_text(locator, text)
            else:
                raise ValueError(f"Missing locator or value for field '{field_id}'")

    def clear_field(self, label):
        """
        Clears the field using standard clearing plus keyboard actions.
        """
        locator = self.elements[label]
        field = self.driver.find_element(*locator)
        field.clear()
        field.send_keys(Keys.CONTROL + 'a')
        field.send_keys(Keys.DELETE)

    def submit(self):
        """
        Clicks the Submit button to attempt to save the edited contact.
        """
        self.click_button(self.elements['submit'])

    def submit_and_wait(self):
        """
        Clicks the Submit button and waits until it disappears from the page,
        indicating that the form is being processed.
        """
        self.click_button(self.elements['submit'])
        WebDriverWait(self.driver, 5).until(
            EC.invisibility_of_element_located(self.elements['submit'])
        )

    def cancel(self):
        """
        Clicks the Cancel button to discard changes.
        """
        self.click_button(self.elements['cancel'])

    def is_error_displayed(self, message):
        """
        Checks whether an error message is present and matches the expected text.
        :param message: Expected error message text.
        :return:True if the error is present and text matches; False otherwise.
        """
        if not self.is_element_present(self.error):
            return False
        return self.is_text_correct(self.error, message)

    def is_edit_successful(self):
        """
        Checks that the edit was successful:
        - No error message is displayed.
        - User is redirected to the Contact Details page.
        :return:True if the edit is successful; False otherwise.
        """
        if self.is_element_present(self.error):
            return False
        return self.is_url_correct(Env.URL_ContactDetails)
