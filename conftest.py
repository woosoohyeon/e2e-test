import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import configs.config as config

@pytest.fixture(scope='session')
def driver():
    _driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    _driver.set_window_size(1920, 1280)
    _driver.implicitly_wait(5)
    yield _driver
    # _driver.close()