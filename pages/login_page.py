from loguru import logger
from test_data.env import Env
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from pages.contact_list_page import ContactListPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.error = (By.ID, 'error')
        self.error_text = 'Incorrect username or password'
        self.elements = {
            'title': (By.TAG_NAME, 'h1'),
            'email': (By.ID, 'email'),
            'password': (By.ID, 'password'),
            'submit': (By.ID, 'submit'),
            'signup': (By.ID, 'signup'),
        }

    def is_login_page(self):
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
        self.input_text(self.elements["email"], email)
        self.input_text(self.elements["password"], password)
        self.click_button(self.elements["submit"])
        return ContactListPage(self.driver, self.url)

    def login_as(self, email, password):
        # Login with defined credentials
        self.open()
        self.complete_login(email, password)

    def is_login_successful(self):
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(Env.URL_ContactList)
        )
        return True

    def is_error_present(self):
        return self.is_element_present(self.error)

    def is_error_text_correct(self):
        return self.is_text_correct(self.error, self.error_text)

    def click_signup(self):
        """
        Clicks [SignUp] button to redirect to AddUser page
        """
        from pages.add_user_page import AddUserPage
        self.click_button(self.elements["signup"])
        return AddUserPage(self.driver, self.url)
