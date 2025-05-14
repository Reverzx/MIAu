from pages.edit_contact_page import EditContactPage
from test_data.env import Env
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from loguru import logger


class ContactDetailsPage(BasePage):
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
            'edit-contact': (By.ID, 'edit-contact'),
            'delete': (By.ID, 'delete'),
            'return': (By.ID, 'return'),
            'logout': (By.ID, 'logout'),
        }
        self.logout_button = (By.ID, 'logout')
        self.return_button = (By.ID, 'return')

    def navigate_to_contact_details_page(self, email, password):
        from pages.contact_list_page import ContactListPage
        contact_list = ContactListPage(self.driver, Env.URL_ContactList)
        contact_list_page = contact_list.navigate_to_contact_list_page(email, password)
        return contact_list_page.navigate_to_contact_details_page()

    def is_contact_details_page(self):
        return self.is_url_correct(Env.URL_ContactDetails)

    def navigate_to_edit_contact_page(self):
        """
        Clicks the Edit Contact button and navigates to the Edit Contact page.
        :return: EditContactPage object
        """
        self.click_button(self.elements['edit-contact'])
        return EditContactPage(self.driver, self.url)

    def is_navigate_to_edit_contact_page_successful(self):
        """
        Waits up to 5 seconds for a successful redirect to the Edit Contact page.
        :return: bool: True if the current URL matches the Edit Contact page url,
        otherwise False.
        """
        WebDriverWait(self.driver, 5).until(
            EC.url_to_be(Env.URL_EditContact)
        )
        return True

    def assert_contact_details_are_correct(self, data):
        """
        Asserts that the contact details match the expected values.
        :param data: Dictionary of field IDs and expected values.
        :return: AssertionError: If any value does not match the expected.
        """
        for field_id, expected_value in data.items():
            locator = self.elements.get(field_id)
            if locator:
                assert self.is_text_correct(locator, expected_value)
            else:
                logger.warning(f"Field '{field_id}' not found in the elements list.")
        logger.success("Contact details match expected values.")

    def delete_contact(self):
        self.click_button(self.elements['delete'])
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            logger.success("Contact deleted successfully.")
        except Exception as e:
            logger.error("Failed to delete contact:", e)

    def cancel_delete_contact(self):
        """
        Deletes the contact by clicking the Delete button and cancel the alert.
        """
        self.click_button(self.elements['delete'])
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            logger.info("Alert dismissed successfully.")
        except NoAlertPresentException:
            logger.error("No alert was present to cancel.")
        except Exception as e:
            logger.error("An unexpected error occurred while attempting to dismiss the alert:", e)

    def logout(self):
        """
        Clicks the Logout button and redirects to the Login page.
        """
        self.click_button(self.elements['logout'])

    def click_return(self):
        """
        Clicks the Return to Contact List button and
        redirects to the Contact List page.
        """
        self.click_button(self.return_button)
