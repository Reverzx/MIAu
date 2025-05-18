from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from test_data.env import Env


class AddUserPage(BasePage):

    first_name_input = (By.CSS_SELECTOR, '[id="firstName"]')
    last_name_input = (By.CSS_SELECTOR, '[id="lastName"]')
    email_input = (By.CSS_SELECTOR, '[id="email"]')
    password_input = (By.CSS_SELECTOR, '[id="password"]')
    submit_bttn = (By.CSS_SELECTOR, '[id="submit"]')
    cancel_bttn = (By.CSS_SELECTOR, '[id="cancel"]')
    error = (By.CSS_SELECTOR, '[id="error"]')
    err_registered_msg = 'Email address is already in use'
    err_fname_msg = 'User validation failed: firstName: Path `firstName` is required.'
    err_lname_msg = 'User validation failed: lastName: Path `lastName` is required.'
    err_email_msg = 'User validation failed: email: Email is invalid'
    err_password_msg = 'User validation failed: password: Path `password` is required.'

    def __init__(self, driver, url):
        super().__init__(driver, url)

    def is_add_user_page(self):
        """
        Check if the current URL is equal with Add User page.
        Returns True if URL is correct, otherwise False.
        """
        return self.is_url_correct(Env.url_add_user)

    def fill_the_registration_form(self, first_name, last_name, email, password):
        """
        Fills the fields with provided values
        """
        self.input_text(self.first_name_input, first_name)
        self.input_text(self.last_name_input, last_name)
        self.input_text(self.email_input, email)
        self.input_text(self.password_input, password)

    def submit(self):
        """
        Clicks sibmit button
        """
        self.click_button(self.submit_bttn)

    def cancel(self):
        """
        Clicks cancel button
        """
        self.click_button(self.cancel_bttn)

    def is_signup_successful(self):
        """
        Waits for 5 seconds for the current URL to match the Contact List page url,
        indicating a successful registration.
        Returns True if URL is correct, otherwise False.
        """
        WebDriverWait(self.driver, 5).until(EC.url_to_be(Env.URL_ContactList))
        return True

    def is_error_text_correct(self, err_text):
        """
        Checks if the displayed error message equal with expected text.
        Returns True if the message is correct, otherwise False.
        """
        return self.is_text_correct(self.error, err_text)
