import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(5)

driver.set_window_size(1920, 1280)
# driver.maximize_window()


class Test_테스트_그룹:
    def test_일_더하기_일은_2다(self):
        driver.get('http://www.naver.com')
        assert 1 + 1 == 2

    def test_0으로_나누기_에러(self):
        with pytest.raises(ZeroDivisionError):
            1 / 0

    def test_재귀_에러(self):
        with pytest.raises(RuntimeError) as excinfo:

            def f():
                f()

            f()
        assert "maximum recursion" in str(excinfo.value)
