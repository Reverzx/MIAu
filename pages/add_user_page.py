from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.contact_list_page import ContactListPage
from test_data.env import Env
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        return self.is_url_correct(Env.url_add_user)


    def add_new_user(self, f_name, l_name, email, password):
        self.input_text(self.first_name_input, f_name)
        self.input_text(self.last_name_input, l_name)
        self.input_text(self.email_input, email)
        self.input_text(self.password_input, password)
        self.click_button(self.submit_bttn)
        return ContactListPage(self.driver, self.url)


    def cancel_add_user(self, f_name, l_name, email, password):
        self.input_text(self.first_name_input, f_name)
        self.input_text(self.last_name_input, l_name)
        self.input_text(self.email_input, email)
        self.input_text(self.password_input, password)
        self.click_button(self.cancel_bttn)
        return LoginPage(self.driver, url=f'{self.url}"login"')


    def if_signup_successful(self):
        WebDriverWait(self.driver, 5).until(EC.url_to_be(Env.URL_ContactList))
        return True


    def is_error_present(self):
        return self.is_element_present(self.error)


    def is_error_text_correct(self, err_text):
        return self.is_text_correct(self.error, err_text)
