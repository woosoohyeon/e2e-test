import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='session')
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.set_window_size(1920, 1280)
    driver.implicitly_wait(5)
    yield driver