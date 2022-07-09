import pytest
from utils.BasicTest import BasicTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# URLs
HOME_URL = 'https://sellercenter.line-beta.biz/@743qocoj/'
BUNDLE_URL = 'https://sellercenter.line-beta.biz/@743qocoj/marketing/bundle'
BUNDLE_ADD_URL = 'https://sellercenter.line-beta.biz/@743qocoj/marketing/bundle/add'
# verify values
BUNDLE_ADD_TITLE = '번들 할인 생성'
BUNDLE_DISCOUNT_PRODUCTS_TITLE = '번들 할인 상품'
MODAL_SELECT_PRODUCT = '상품 선택'
# Input Values
SAMPLE_ADDBUNNDLE_NAME = '[qa] 자동화 번들 등록 test'

SAMPLE_DATE = '2022.06.01 ~ 2022.06.30'
SAMPLE_BUNNDLE_COUNT = 1
SAMPLE_BUNNDLE_TYPE = '2 개 사면 $10 할인'
SAMPLE_PRODUCT = 2
# SAMPLE_ORDERS = 0 -> 숫자 여부만 확인하면 됨
SAMPLE_PERIOD = {
  'start-time': '2022.07.01 / 14:53',
  'end-time': '2022.07.02 / 14:52'
}
SAMPLE_STATUS = 'Upcoming'
SAMPLE_ACTION = '수정삭제'

class TestViewBundleDiscount(BasicTest):
  resource='/marketing/bundle'

  @pytest.fixture(scope='class', autouse=True)
  def login(self, driver):
    self._move(driver, '', By.LINK_TEXT, '비즈니스 계정으로 로그인')
    self._find(driver, By.NAME, 'email').send_keys(self.seller_id)
    self._find(driver, By.NAME, 'password').send_keys(self.seller_pw)
    self._find(driver, By.XPATH, '/html/body/div[2]/div/div[3]/div/div[3]/div[2]/form/div/div[5]/button').click()
  
  @pytest.fixture(scope='class', autouse=True)
  def translate_korean(self, driver):
    self._wait(driver, By.XPATH, '//*[@id="footer"]/div[2]/div').click()
    self._find(By.XPATH, '//*[@id="footer"]/div[2]/div/div[2]/div/span[3]').click()

  def test_ATC_01_BundleSearchCheck(self, driver):
    SAMPLE_START_DATE='2022-07-01'
    SAMPLE_END_DATE='2022-07-08'
    SAMPLE_BUNNDLE_NAME='[qa] 자동화 test - 종료일'
    SAMPLE_BUNNDLE_ID = '100000834'

    self._move(driver, '/marketing/bundle', By.CLASS_NAME, 'search_area')

    # 1. 검색 조건 : 일자 (시작일) & 번들 이름
    # 일자> 시작일 선택 
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]').click()
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div/span[1]').click()
    # datepicker 클릭
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/input').click()
    self._wait(driver, By.CLASS_NAME, 'mx-datepicker-main')
    # 기간 선택
    self._find(driver, By.XPATH, f"//td[@title='{SAMPLE_START_DATE}']").click()
    self._find(driver, By.XPATH, f"//td[@title='{SAMPLE_END_DATE}']").click()
    # 검색 조건> 번들 이름 선택
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]').click()
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/span[1]').click()
    # 검색어 입력
    self._find(driver, By.CSS_SELECTOR, '.input_area.is_search.search_input>input').send_keys(SAMPLE_BUNNDLE_NAME)
    # 검색 버튼 클릭
    self._find(driver, By.XPATH, "//button[@aria-label='Search']").click()
    time.sleep(3)
    #검색 필드 초기화
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/button[2]').click()
    time.sleep(1)

    #2. 검색 조건 : 일자 (종료일) & 번들 ID
    # 일자> 종료일 선택
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]').click()
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div/span[2]').click()
    # datepicker 클릭
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/input').click()
    time.sleep(1)
    # 기간 선택
    self._find(driver, By.XPATH, f"//td[@title='{SAMPLE_START_DATE}']").click()
    self._find(driver, By.XPATH, f"//td[@title='{SAMPLE_END_DATE}']").click()
    # 검색 조건> 번들 ID 선택
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]').click()
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/span[2]').click()
    # 검색어 입력
    self._find(driver, By.CSS_SELECTOR, '.input_area.is_search.search_input>input').send_keys(SAMPLE_BUNNDLE_ID)
    # 검색 버튼 클릭
    self._find(driver, By.XPATH, "//button[@aria-label='Search']").click() 

  def test_ATC_02_BundleResultsCheck(self, driver):
    SAMPLE_BUNNDLE_ID = '100000834'
    SAMPLE_BUNNDLE_NAME='[qa] 자동화 test - 종료일'

    time.sleep(2)
    bs = BeautifulSoup(driver.page_source, 'html.parser')

    product_table = bs.select_one('.product_table')
    table_list = []
    table_body = product_table.find('tbody')
    rows = table_body.find_all('tr')
    
    for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      table_list.append([ele for ele in cols if ele])
    
    first_row = table_list[0]
    _1, period_start, _2, period_end = first_row[4].split('\n')
    period_start = period_start.strip()
    period_end = period_end.strip()

    # 번들 카운트 노출 확인
    bundle_count = bs.select_one('p.result > em.num')
    assert int(bundle_count.get_text()) == SAMPLE_BUNNDLE_COUNT, "번들 카운트 노출 확인"

    # 번들 목록 노출 확인 (1행만)
    assert SAMPLE_BUNNDLE_ID in first_row[0], "번들 id 확인"
    assert SAMPLE_BUNNDLE_NAME in first_row[0], "번들 이름 확인"
    assert first_row[1] == SAMPLE_BUNNDLE_TYPE, "번들 타입 확인"
    assert int(first_row[2]) == SAMPLE_PRODUCT, "상품 확인"
    assert first_row[3].isdigit(), "적용 수 확인"
    assert period_start == SAMPLE_PERIOD['start-time'], "기간 확인(시작일)"
    assert period_end == SAMPLE_PERIOD['end-time'], "기간 확인(종료일)"
    assert first_row[5] == SAMPLE_STATUS, "상태 확인"
    assert first_row[6] == SAMPLE_ACTION, "동작 확인"

  def test_ATC_03_BundleStatusFilteringCheack(self, driver):
    #검색 필드 초기화
    self._find(driver, By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/button[2]').click()
    time.sleep(3)

    #상태 필터링 클릭 > 선택한 필터링 별 번들 목록 노출 확인
    # 1. Upcoming 클릭 
    self._find(driver, By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/button').click()
    self._find(driver, By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/div/div/span[2]').click()
    time.sleep(1)

    #table의 상태값이 upcoming이면 pass되어야 함
    ###
    ###
    ###

    # 2. Ongoing 클릭
    self._find(driver, By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/button').click()
    self._find(driver, By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/div/div/span[3]').click()
    time.sleep(1)

    #table의 상태값이 upcoming이면 pass되어야 함
    ###
    ###
    ###

    # 3 .Expired 클릭
    self._find(driver, By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/button').click()
    self._find(driver, By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/div/div/span[4]').click()
    time.sleep(1)

    #table의 상태값이 upcoming이면 pass되어야 함
    ###
    ###
    ###

  #def test_ATC_04_ActionFieldButtonCheck():
    ###
    ###
    ###