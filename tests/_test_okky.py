import pytest
from utils.BasicTest import BasicTest
from selenium.webdriver.common.by import By

class TestLogin(BasicTest):
    resource='/login/auth?redirectUrl=%2F'

    # 클래스 단위로 자동실행
    @pytest.fixture(scope='class', autouse=True)
    def init(self):
        print('init TestLogin')

    def test_login(self, driver):
        self._move(driver, self.resource, By.ID, 'username')
        self._find(driver, By.ID, 'username').send_keys('rjadms1028')
        self._find(driver, By.CLASS_NAME, 'password').send_keys('1234')
        self._find(driver, By.ID, 'btnUserLogin').click()