from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.alert import Alert

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

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

# chrome_options = Options()
# chrome_options.add_argument("--headless")

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def table_parser(table):
  data = []
  table_body = table.find('tbody')
  rows = table_body.find_all('tr')
  for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
  return data

def init():
  driver.implicitly_wait(5)
  driver.set_window_size(1920, 1200)

def destory():
  driver.quit()

def login():
  print('Seller Center 로그인')
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
  
  ####번들 페이지 이동 (삭제 예정)
  driver.get(BUNDLE_URL)
  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'search_area')))

def ATC_01_BundleSearchCheck():
  print(bcolors.HEADER + 'ATC_01_검색 영역 노출 및 검색 동작 확인' + bcolors.ENDC)
  driver.get(BUNDLE_URL)
  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'search_area')))

  # 일자> 시작일 선택 
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div/span[1]').click()
  # datepicker 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/input').click()
  time.sleep(1)
  # 기간 선택
  driver.find_element(By.XPATH, "//td[@title='{}']".format(SAMPLE_START_DATE)).click()
  driver.find_element(By.XPATH, "//td[@title='{}']".format(SAMPLE_END_DATE)).click()
  # 검색 조건> 번들 이름 선택
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/span[1]').click()
  # 검색어 입력
  driver.find_element(By.CSS_SELECTOR, '.input_area.is_search.search_input>input').send_keys(SAMPLE_BUNNDLE_NAME)
  # 검색 버튼 클릭
  driver.find_element(By.XPATH, "//button[@aria-label='Search']").click()
  time.sleep(3)
  #검색 필드 초기화
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/button[2]').click()
  time.sleep(1)

  # 일자> 종료일 선택
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div/span[2]').click()
  # datepicker 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/input').click()
  time.sleep(1)
  # 기간 선택
  driver.find_element(By.XPATH, "//td[@title='{}']".format(SAMPLE_START_DATE)).click()
  driver.find_element(By.XPATH, "//td[@title='{}']".format(SAMPLE_END_DATE)).click()
  # 검색 조건> 번들 ID 선택
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/span[2]').click()
  # 검색어 입력
  driver.find_element(By.CSS_SELECTOR, '.input_area.is_search.search_input>input').send_keys(SAMPLE_BUNNDLE_ID)
  # 검색 버튼 클릭
  driver.find_element(By.XPATH, "//button[@aria-label='Search']").click()  

def ATC_02_BundleResultsCheck():
  print(bcolors.HEADER + 'ATC_02_검색된 번들 카운트 및 목록 확인' + bcolors.ENDC)

  time.sleep(2)
  bs = BeautifulSoup(driver.page_source, 'html.parser')

  # 번들 카운트 노출 확인
  bundle_count = bs.select_one('p.result > em.num')
  print('번들 카운트 노출 확인: {}'.format('확인됨' if int(bundle_count.get_text()) == SAMPLE_BUNNDLE_COUNT else '실패'))

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
  # 번들 목록 노출 확인 (1행만)
  print('번들 id 확인: {}'.format('정상' if SAMPLE_BUNNDLE_ID in first_row[0] else '에러'))
  print('번들 이름 확인: {}'.format('정상' if SAMPLE_BUNNDLE_NAME in first_row[0] else '에러'))
  print('번들 타입 확인: {}'.format('정상' if first_row[1] == SAMPLE_BUNNDLE_TYPE else '에러'))
  print('상품 확인: {}'.format('정상' if int(first_row[2]) == SAMPLE_PRODUCT else '에러'))
  print('적용 수 확인: {}'.format('정상' if first_row[3].isdigit() else '에러'))
  print('기간 확인(시작일): {}'.format('정상' if period_start == SAMPLE_PERIOD['start-time'] else '에러'))
  print('기간 확인(종료일): {}'.format('정상' if period_end == SAMPLE_PERIOD['end-time'] else '에러'))
  print('상태 확인: {}'.format('정상' if first_row[5] == SAMPLE_STATUS else '에러'))
  print('동작 확인: {}'.format('정상' if first_row[6] == SAMPLE_ACTION else '에러'))

def ATC_03_BundleStatusFilteringCheack():
  print(bcolors.HEADER + 'ATC_03_상태 필터링 동작 확인' + bcolors.ENDC)
  #검색 필드 초기화
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/button[2]').click()
  time.sleep(1)

  #상태 필터링 클릭 > 선택한 필터링 별 번들 목록 노출 확인
  # 1. Upcoming 클릭 
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/button').click()
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/div/div/span[2]').click()
  time.sleep(1)
  #table의 상태값이 upcoming이면 pass되어야 함

  # 2. Ongoing 클릭
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/button').click()
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/div/div/span[3]').click()
  time.sleep(1)
  # 3 .Expired 클릭
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/button').click()
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/thead/tr/th[6]/div/div/div/span[4]').click()
  time.sleep(1)

def ATC_04_ActionFieldButtonCheck():
  print(bcolors.HEADER + 'ATC_04_Action 필드 동작 확인' + bcolors.ENDC)
  ##########
  ##########
  ##########

def ATC_05_FindAddBundlePage():
  print(bcolors.HEADER +'ATC_05_번들 디스카운트 등록 페이지 노출 확인' + bcolors.ENDC)

  #[번들 할인 추가] 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[1]/div[2]/button').click()

  #번들 할인 생성 페이지 URL 확인
  print('번들 할인 생성 페이지 이동 확인: {}'.format('정상' if BUNDLE_ADD_URL == driver.current_url else '에러'))

  #번들 할인 생성 페이지 타이틀 노출 확인
  title = driver.find_element(By.XPATH, '//*[@id="content"]/div/header/div/h2').text
  print('번들 할인 생성 페이지 타이틀 확인: {}'.format('정상' if BUNDLE_ADD_TITLE == title else '에러'))
  

def ATC_06_ModifyBundleProduct():
  print(bcolors.HEADER +'ATC_06_번들 할인 상품 등록/삭제/정렬 동작 확인' + bcolors.ENDC)

  #번들 할인 상품 영역 노출 확인
  title = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[2]/div/h3').text
  print('번들 할인 상품 타이틀 확인: {}'.format('정상' if BUNDLE_DISCOUNT_PRODUCTS_TITLE == title else '에러'))

  #[상품등록] 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[2]/div/button/span').click()

  #상품 선택 모달창 노출 확인
  modal_title = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div/header/h1').text
  print('상품 선택 모달창 타이틀 확인: {}'.format('정상' if MODAL_SELECT_PRODUCT == modal_title else '에러'))

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
  time.sleep(3)


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

def ATC_07_WirteBundleField():
  print(bcolors.HEADER + 'ATC_07_번들 디스카운트 등록 페이지 필드 입력 확인' + bcolors.ENDC)

  #번들 이름 입력
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[2]/div[2]/div/input').send_keys(SAMPLE_ADDBUNNDLE_NAME)

  #기간 선택 (시작일시)
  #시작 날짜 선택
  driver.find_element(By.XPATH, '//*[@id="startDate"]/div/input').click()
  time.sleep(1)
  driver.find_element(By.XPATH, "//td[@title='{}']".format(SAMPLE_START_DATE)).click()
  time.sleep(1)

  #시작 시간 선잭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div/span[1]').click()
  time.sleep(1)

  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[1]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/div/span[1]').click()
  time.sleep(1)


  #기간 선택 (종료일)
  #정료 날짜 선택
  driver.find_element(By.XPATH, '//*[@id="endDate"]/div/input').click()
  time.sleep(1)
  driver.find_element(By.XPATH, "//td[@title='{}']".format(SAMPLE_END_DATE)).click()
  time.sleep(1)

  #종료 시간 선잭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/span[24]').click()
  time.sleep(1)

  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/div[1]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div/span[60]').click()
  time.sleep(1)

  #번들 타입 선택 (수량조건)
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[4]/div[2]/span[1]/label').click()

  #번들 타입 별 구매 조건 선택
  #1. 정액할인 선택
  #driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[4]/div[3]/div[1]/span[1]/label').click()

  #2. 정률할인 선택
  #driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[4]/div[3]/div[1]/span[2]/label').click()

  #3. 번들가격 선택
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[4]/div[3]/div[1]/span[3]/label').click()
  
  #구매조건 input box 입력 (공통)
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[4]/div[3]/div[2]/div[1]/div/div/input').send_keys('2')
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[4]/div[3]/div[2]/div[2]/div/div/input').send_keys('10')

  #구매횟수 제한 선택
  #1. 무제한 선택
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[5]/div[2]/span/label').click()
  
  #2. N회 선택
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[5]/div[2]/div/span/label').click()
  #2-1. 구매 횟수 최대 N회 선택 시, N 입력
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[1]/div[5]/div[2]/div/div/div/div/input').send_keys('10')

  #번들 할인 상품 등록 
  #[상품등록] 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[2]/div/button/span').click()

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

def ATC_08_AddBundleCheck():
  print(bcolors.HEADER + 'ATC_08_번들 디스카운트 정책 등록 확인' + bcolors.ENDC)

  #[저장] 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[3]/div/button[2]').click()

  #저장 확인 얼럿 노출 확인 
  try:
    confirm_alert = Alert(driver)
    confirm_alert.accept()

  except:
    print("no alert")
  time.sleep(2)

  #번들 추가 얼럿 노출 확인
  try:
    confirm_alert = Alert(driver)
    confirm_alert.accept()

  except:
    print("no alert")
  time.sleep(2)

  #번들 할인 목록 페이지 URL 이동 확인
  print('번들 할인 목록 페이지 이동 확인: {}'.format('정상' if BUNDLE_URL == driver.current_url else '에러'))

  #번들 count +1 확인
  #####
  #####

  #등록한 번들 목록 노출 확인 
  # 일자> 시작일 선택 
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div/span[1]').click()
  # datepicker 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/input').click()
  time.sleep(1)
  # 기간 선택
  driver.find_element(By.XPATH, "//td[@title='{}']".format(SAMPLE_START_DATE)).click()
  driver.find_element(By.XPATH, "//td[@title='{}']".format(SAMPLE_END_DATE)).click()
  # 검색 조건> 번들 이름 선택
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div/span[1]').click()
  # 검색어 입력
  driver.find_element(By.CSS_SELECTOR, '.input_area.is_search.search_input>input').send_keys(SAMPLE_ADDBUNNDLE_NAME)
  # 검색 버튼 클릭
  driver.find_element(By.XPATH, "//button[@aria-label='Search']").click()
  time.sleep(3)

  findbundle_name = driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/table/tbody/tr/td[1]/strong').text
  print('등록한 번들 목록 노출 확인: {}'.format('확인됨' if findbundle_name == SAMPLE_ADDBUNNDLE_NAME else '실패'))

init()
login()
ATC_01_BundleSearchCheck()
ATC_02_BundleResultsCheck()
ATC_03_BundleStatusFilteringCheack()
ATC_04_ActionFieldButtonCheck()
ATC_05_FindAddBundlePage()
ATC_06_ModifyBundleProduct()
ATC_07_WirteBundleField()
ATC_08_AddBundleCheck()
# destory()