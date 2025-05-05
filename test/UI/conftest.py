from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from loguru import logger
import sys
from test_data.env import Env
from test_data.user_creds import UserCredentials


def pytest_configure(config):
    logger.remove()
    logger.add(sys.stdout, level='INFO')


@pytest.fixture
def driver():
    logger.info("Launching headless-browser")
    _options = webdriver.ChromeOptions()
    _options.add_argument("--headless")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    _options.add_experimental_option("prefs", prefs)
    _options.add_argument("--incognito")
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=_options
    )
    browser.implicitly_wait(5)
    yield browser
    logger.info("Closing browser")
    browser.quit()
