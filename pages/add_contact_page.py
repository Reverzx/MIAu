from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from test_data.env import Env


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
        self.error = (By.ID, 'error')
        self.error_fname_msg = 'Contact validation failed: firstName: Path `firstName` is required.'
        self.error_lname_msg = 'Contact validation failed: lastName: Path `lastName` is required.'
        self.error_bdate_msg = 'Contact validation failed: birthdate: Birthdate is invalid'
        self.error_email_msg = 'Contact validation failed: email: Email is invalid'
        self.error_phone_msg = 'Contact validation failed: phone: Phone number is invalid'
        self.error_postcode_msg = 'Contact validation failed: postalCode: Postal code is invalid'

        self.logout_button = (By.ID, 'logout')
        self.cancel_button = (By.ID, 'cancel')
        self.submit_button = (By.ID, 'submit')

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

    def is_error_text_correct(self, err_text):
        """
        Checks if the displayed error message equal with expected text.
        Returns True if the message is correct, otherwise False.
        """
        return self.is_text_correct(self.error, err_text)

    def submit(self):
        self.click_button(self.elements['submit'])

    def logout(self):
        self.click_button(self.logout_button)

    def cancel(self):
        """
        Clicks the Logout button and redirects to the Contact List page.
        """
        self.click_button(self.cancel_button)

    def login_and_add_contact(self, driver, email, password, new_cont):
        from pages.login_page import LoginPage
        from pages.contact_list_page import ContactListPage
        logpage = LoginPage(driver, Env.URL_Login)
        logpage.open()
        contlist = logpage.complete_login(email, password)
        add_cont = contlist.navigate_to_add_contact_page()
        add_cont.fill_contact_form(new_cont)
        add_cont.submit()
        return ContactListPage(self.driver, self.url)

    def login_and_cancel_add_contact(self, driver, email, password, new_cont):
        from pages.login_page import LoginPage
        from pages.contact_list_page import ContactListPage
        logpage = LoginPage(driver, Env.URL_Login)
        logpage.open()
        contlist = logpage.complete_login(email, password)
        add_cont = contlist.navigate_to_add_contact_page()
        add_cont.fill_contact_form(new_cont)
        add_cont.cancel()
        return ContactListPage(self.driver, self.url)

    def is_addition_successful(self):
        """
        Waits for 5 seconds for the current URL to match the Contact List page url,
        indicating a successful registration.
        Returns True if URL is correct, otherwise False.
        """
        WebDriverWait(self.driver, 5).until(EC.url_to_be(Env.URL_ContactList))
        return True
