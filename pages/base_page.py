from selenium.common import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from loguru import logger


class BasePage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)

    def is_url_correct(self, url, timeout=5):
        """
        Waits up to the specified timeout for the current URL to match the expected URL.
        :return: bool: True if the current URL matches the expected URL, otherwise False.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_to_be(url)
            )
            return True
        except TimeoutException:
            logger.warning(f"URL did not match expected: {url}")
            return False

    def is_element_present(self, locator):
        """
        Checks whether the specified element is present on the page.
        :param locator: A locator tuple (By, value) used to find the element.
        :return: bool: True if the element is present, otherwise False.
        """
        return bool(self.driver.find_elements(*locator))

    def is_text_correct(self, locator, text, timeout=5):
        """
        Waits up to the specified timeout for the element to become visible,
        then checks whether its text matches the expected value.
        :param locator: A locator tuple (By, value) used to find the element.
        :param text: The expected text to compare with.
        :return: bool: True if the element's text matches the expected text,
        otherwise False.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.text.strip() == text
        except TimeoutException:
            logger.warning(f"Text did not match expected. Expected text: {text}")
            return False

    def input_text(self, locator, text):
        """
        Clears the existing value and inputs the specified text into the target element.
        :param locator: A locator tuple (By, value) used to find the element.
        :param text: The value to enter into the field.
        :return: None
        """
        field = self.driver.find_element(*locator)
        field.clear()
        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.DELETE)
        field.send_keys(text)

    def click_button(self, locator, timeout=5):
        """
        Waits up to the specified timeout for the button to become clickable,
        then clicks the button.
        :param locator: A locator tuple (By, value) used to find the element.
        :return: None
        """
        try:
            button = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            button.click()
        except TimeoutException:
            logger.warning(f"Button not clickable: {locator}")
            raise

    def locate_element(self, locator):
        return self.driver.find_element(*locator)


    def is_text_present(self, locator, text):
        try:
            self.driver.find_element(By.XPATH, f'//{locator}[contains(text(), "{text}")]')
            return True
        except NoSuchElementException:
            logger.warning(f'Text {text} is not found')
            return False
