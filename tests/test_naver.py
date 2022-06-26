def test_일_더하기_일은_2다(driver):
    driver.get('http://www.naver.com')
    assert 1 + 1 == 2, "일 더하기 일은 2다."
