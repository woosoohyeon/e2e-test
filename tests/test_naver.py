import configs.config as ENV

class TestNaver:
    MAIN_URL = ENV.NAVER_URL

    def test_one(self):
        assert self.MAIN_URL == 'https://www.naver.com', '네이버 주소 확인'
