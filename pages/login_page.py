from loguru import logger
from pages.base_page import BasePage
from pages.contact_list_page import ContactListPage
from test_data.env import Env
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.email = (By.ID, 'email')
        self.password = (By.ID, 'password')
        self.submit = (By.ID, 'submit')
        self.error = (By.ID, 'error')
        self.signup = (By.ID, 'signup')
        self.error_text = 'Incorrect username or password'
        self.elements = {
            'title': (By.TAG_NAME, 'h1'),
            'email': (By.ID, 'email'),
            'password': (By.ID, 'password'),
            'submit': (By.ID, 'submit'),
            'signup': (By.ID, 'signup'),
        }

    def is_login_page(self):
        """
        Checks whether the current URL matches the login page URL.
        :return: bool: True if the current URL is correct, otherwise False.
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.url_matches(Env.URL_Login)
            )
            return True
        except TimeoutException:
            logger.warning(f"Timeout: Current URL is {self.driver.current_url}, "
                           f"expected was {Env.URL_Login}")
            return False

    def complete_login(self, email, password):
        """
        Fills in the email and password fields with provided values,
        clicks the submit button, and check if the page redirects
        to the Contact List page.
        :return: bool: True if the current URL matches the Contact List page url,
        otherwise False.
        """
        self.input_text(self.email, email)
        self.input_text(self.password, password)
        self.click_button(self.submit)
        return ContactListPage(self.driver, self.url)

    def login_as(self, email, password):
        """
        Opens the Login page, fills in the email and password fields,
        and submits the login form using the provided credentials.
        :return: bool: True if the current URL matches the Contact List page url,
        otherwise False.
        """
        self.open()
        self.complete_login(email, password)

    def is_login_successful(self):
        """
        Waits up to 5 seconds for the current URL to match the Contact List page url,
        indicating a successful loging.
        :return: bool: True if the current URL matches the Contact List page url,
        otherwise False.
        """
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(Env.URL_ContactList)
        )
        return True

    def is_error_present(self):
        """
        Checks whether the error message is displayed on the page.
        :return: bool: True if the error message is displayed, otherwise False.
        """
        return self.is_element_present(self.error)

    def is_error_text_correct(self):
        """
        Checks whether the displayed error message text matches the expected value.
        :return: bool: True if the error message text matches the expected text,
        otherwise False.
        """
        return self.is_text_correct(self.error, self.error_text)

    def click_signup(self):
        """
        Clicks [SignUp] button to redirect to AddUser page
        """
        from pages.add_user_page import AddUserPage
        self.click_button(self.signup)
        return AddUserPage(self.driver, self.url)
