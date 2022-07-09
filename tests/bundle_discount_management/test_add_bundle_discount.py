from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
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
SELLER_ID = "gstw0011@gmail.com"
SELLER_PW = "linegift123"
SAMPLE_BUNNDLE_ID = '100000834'
SAMPLE_BUNNDLE_NAME = '[qa] 자동화 test - 종료일'
SAMPLE_ADDBUNNDLE_NAME = '[qa] 자동화 번들 등록 test'
SAMPLE_START_DATE = '2022-07-01'
SAMPLE_END_DATE = '2022-07-08'
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

def test_login(driver):
  driver.get(HOME_URL)
  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.LINK_TEXT, '비즈니스 계정으로 로그인'))).click()
  driver.find_element(By.NAME, 'email').send_keys(SELLER_ID)
  driver.find_element(By.NAME, 'password').send_keys(SELLER_PW)
  driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div/div[3]/div[2]/form/div/div[5]/button').click()

  # 한국어 변경
  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="footer"]/div[2]/div'))).click()
  driver.find_element(By.XPATH, '//*[@id="footer"]/div[2]/div/div[2]/div/span[3]').click()

  # 파일명 가져와서 캡쳐 따기
  # /screenshot/filename/함수이름_설명.png
  
  # 번들 페이지 이동 (삭제 예정)
  driver.get(BUNDLE_URL)
  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'search_area')))
  assert driver.find_element(By.CLASS_NAME, 'title_lv2').text == '번들 할인 목록', '번들 페이지 이동 확인'

def test_ATC_05_FindAddBundlePage(driver):
  #ATC_05_번들 디스카운트 등록 페이지 노출 확인

  #[번들 할인 추가] 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[1]/div[2]/button').click()

  #번들 할인 생성 페이지 URL 확인
  assert BUNDLE_ADD_URL == driver.current_url, '번들 할인 생성 페이지 이동 확인'

  #번들 할인 생성 페이지 타이틀 노출 확인
  title = driver.find_element(By.XPATH, '//*[@id="content"]/div/header/div/h2').text
  assert BUNDLE_ADD_TITLE == title, '번들 할인 생성 페이지 타이틀 확인'  

def test_ATC_06_ModifyBundleProduct(driver):
  #ATC_06_번들 할인 상품 등록/삭제/정렬 동작 확인

  #번들 할인 상품 영역 노출 확인
  title = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[2]/div/h3').text
  assert BUNDLE_DISCOUNT_PRODUCTS_TITLE == title, '번들 할인 상품 타이틀 확인'  

  #[상품등록] 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[2]/div/button/span').click()

  #상품 선택 모달창 노출 확인
  modal_title = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/header/h1').text
  assert MODAL_SELECT_PRODUCT == modal_title, '상품 선택 모달창 타이틀 확인'  

  #묶음 배송 그룹 선택 (-> 반복문으로 변경 필요함)
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div[1]/div[1]/div[1]/div/div').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div[1]/div[1]/div[1]/div/div[2]/div/span[1]').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div[1]/div/div/button/span').click()

  #번들 할인 등록 상품 선택 (-> 반복문으로 변경 필요함)
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div[1]/div[3]/table/tbody/tr[1]/td[1]/span/label').click()

  #[추가] 버튼 클릭 
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/div[2]/div/button[2]/span').click()

  #얼럿 확인
  try:
    confirm_alert = Alert(driver)
    confirm_alert.accept()

  except:
    print("no alert")
  time.sleep(2)
  #번들 할인 상품 영역 내 상품 추가 확인 

  #등록한 상품 [삭제] 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[2]/div[2]/table/tbody/tr/td[6]/button').click()

  """
  #번들 할인 상품 삭제 확인
  if driver.find_element(By.CLASS_NAME, 'product_table') == null:
    print('삭제동작 확인')
  else:
    print('에러')
  
  #번들 할인 상품 정렬 변경 확인 
  #드로그앤드롭?
  """

  time.sleep(10)