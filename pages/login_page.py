from pages.base_page import BasePage
from pages.contact_list_page import ContactListPage
from test_data.env import Env
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.email = (By.ID, 'email')
        self.password = (By.ID, 'password')
        self.submit = (By.ID, 'submit')
        self.error = (By.ID, 'error')
        self.error_text = 'Incorrect username or password'

    def is_login_page(self):
        return self.is_url_correct(Env.URL_Login)

    def complete_login(self, email, pswrd):
        self.input_text(self.email, email)
        self.input_text(self.password, pswrd)
        self.click_button(self.submit)
        return ContactListPage(self.driver, self.url)

    def login_as(self, email, pswrd):
        self.open()
        self.complete_login(email, pswrd)

    def is_login_successful(self):
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(Env.URL_ContactList)
        )
        return True

    def is_error_present(self):
        return self.is_element_present(self.error)

    def is_error_text_correct(self):
        return self.is_text_correct(self.error, self.error_text)
