from pages.base_page import BasePage


class ContactDetailsPage(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)