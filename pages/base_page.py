from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger


class BasePage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open(self):
        self.driver.get(self.url)

    def is_url_correct(self, url, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_to_be(url)
            )
            return True
        except TimeoutException:
            logger.warning(f"URL did not match expected: {url}")
            return False

    def is_element_present(self, locator):
        return bool(self.driver.find_elements(*locator))

    def is_text_correct(self, locator, text, timeout=5):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.text.strip() == text
        except TimeoutException:
            logger.warning(f"Text did not match expected. Expected text: {text}")
            return False

    def input_text(self, locator, text):
        field = self.driver.find_element(*locator)
        field.clear()
        field.send_keys(text)

    def click_button(self, locator, timeout=5):
        try:
            button = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            button.click()
        except TimeoutException:
            logger.warning(f"Button not clickable: {locator}")
            raise
