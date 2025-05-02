from pages.base_page import BasePage
from pages.contact_list_page import ContactListPage
from selenium.webdriver.common.by import By


class AddContactPage(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)

    def fill_add_contact_form(self):
        pass

    def submit_add_contact_form(self):
        self.fill_add_contact_form()
        return ContactListPage(self.driver, self.url)
