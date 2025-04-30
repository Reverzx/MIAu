from selenium import webdriver
import pytest
from loguru import logger
import sys


def pytest_configure(config):
    logger.remove()
    logger.add(sys.stdout, level='INFO')


@pytest.fixture
def driver():
    logger.info("Launching headless-browser")
    _options = webdriver.ChromeOptions()
    _options.add_argument("--headless")
    _options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(options=_options)
    browser.implicitly_wait(5)
    yield browser
    logger.info("Closing browser")
    browser.quit()
