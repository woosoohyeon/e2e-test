from seleniumbase import BaseCase


class TestMFALogin(BaseCase):
    def test_mfa_login(self):
        self.open("https://seleniumbase.io/realworld/login")
