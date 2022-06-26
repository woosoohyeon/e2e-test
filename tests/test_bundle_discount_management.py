from turtle import home
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from html_table_parser import HTMLTableParser
import pandas as pd
from dotenv import dotenv_values
import time

# URLs
HOME_URL = 'https://sellercenter.line-beta.biz/@743qocoj/'
BUNDLE_URL = 'https://sellercenter.line-beta.biz/@743qocoj/marketing/bundle'

# Input Values
SELLER_ID = "gstw0011@gmail.com"
SELLER_PW = "linegift123"
SAMPLE_BUNNDLE_ID = '100000834'
SAMPLE_BUNNDLE_NAME = '[qa] 자동화 test - 종료일'
SAMPLE_START_DATE = '2022-06-24'
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
  driver.set_window_size(1080, 720)

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

def ATC_01_BundleSearchCheck():
  print('검색 영역 노출 및 검색 동작 확인')
  driver.get(BUNDLE_URL)
  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'search_area')))
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
  print('검색된 번들 카운트 및 목록 확인')
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
  print('상태 필터링 동작 확인')

init()
login()
ATC_01_BundleSearchCheck()
ATC_02_BundleResultsCheck()
ATC_03_BundleStatusFilteringCheack()
# destory()