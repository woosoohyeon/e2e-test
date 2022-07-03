from this import d
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
DISPLAY_CATEGORY_URL = 'https://sellercenter.line-beta.biz/@743qocoj/store/display-categories'
DISPLAY_CATEGORY_TRUE_URL = 'https://sellercenter.line-beta.biz/@743qocoj/store/display-categories?display=true'
DISPLAY_CATEGORY_FALSE_URL = 'https://sellercenter.line-beta.biz/@743qocoj/store/display-categories?display=false'
DISPLAY_CATEGORY_ADD_URL = 'https://sellercenter.line-beta.biz/@743qocoj/store/display-categories/create'
DISPLAY_CATEGORY_EDIT_URL = 'https://sellercenter.line-beta.biz/@743qocoj/store/display-categories/10004704/edit'

# verify values
CATEGOTY_ADD_TITLE = '카테고리 등록'
CATEGOTY_EDIT_TITLE = '카테고리 수정'
BUNDLE_DISCOUNT_PRODUCTS_TITLE = '번들 할인 상품'
MODAL_SELECT_PRODUCT = '상품 선택'
# Input Values
SELLER_ID = "gstw0011@gmail.com"
SELLER_PW = "linegift123"
SMAPLE_SEARCH_KEYWORD = '자동화'
SAMPLE_CATEGORY_NAME = '[qa] 자동화 확인용-수정'
SAMPLE_ADDCATEGORY_NAME = '[qa] 자동화 카테고리 등록 test'
SAMPLE_EDITCATEGORY_NAME = '[qa] 자동화 카테고리 수정 test'
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

  ####전시카테고리 페이지 이동 (삭제 예정)
  driver.get(DISPLAY_CATEGORY_URL)
  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'title_lv2')))

def ATC_01_ListingCategorySearchCheck():
  print(bcolors.HEADER + 'ATC_01_검색 영역 노출 및 검색 동작 확인' + bcolors.ENDC)
  driver.get(DISPLAY_CATEGORY_URL)
  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'title_lv2')))
  #검색 영역 노출 및 검색 동작 확인

  # 전시카테고리명 선택 
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[1]/div[1]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[1]/div[2]/div/span').click()

  #1. 전시 상태 드롭다운 선택 (전체)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[2]/div[1]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span[1]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[3]/button[1]').click()
  print('전시 상태 (전체) 카테고리 확인: {}'.format('정상' if DISPLAY_CATEGORY_URL == driver.current_url else '에러'))

  #2. 전시 상태 드롭다운 선택 (전시중)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[2]/div[1]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span[2]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[3]/button[1]').click()
  print('전시 상태 (전시중) 카테고리 확인: {}'.format('정상' if DISPLAY_CATEGORY_TRUE_URL == driver.current_url else '에러'))

  #3. 전시 상태 드롭다운 선택 (전시중지)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[2]/div[1]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span[3]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[3]/button[1]').click()
  print('전시 상태 (전시중지) 카테고리 확인: {}'.format('정상' if DISPLAY_CATEGORY_FALSE_URL == driver.current_url else '에러'))

  # 전시 상태 변경 (전체)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[2]/div[1]').click()
  time.sleep(1)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span[1]').click()
  time.sleep(1)

  # 검색어 입력 후 검색 버튼 클릭
  driver.find_element(By.CLASS_NAME,'input_text').send_keys(SMAPLE_SEARCH_KEYWORD)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[3]/button[1]').click()
  time.sleep(1)

  #검색어 일치 여부 확인 필요
  ###
  ###

  #검색 필드 새로고침 클릭
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[3]/button[2]').click()


""" def ATC_02_ListingCategoryResultsCheck():
  print(bcolors.HEADER + 'ATC_02_검색된 전시 카테고리 카운트 및 목록 확인' + bcolors.ENDC)

  #전시 카테고리 개수 확인
  ###
  ###

  #count 비교
  ###
  ###

  #전시 카테고리 목록 노출 확인
  ###
  ### """
  #tr의 개수와 비교 작성 

def ATC_03_FindAddListingCategory():
  print(bcolors.HEADER + 'ATC_03_전시 카테고리 등록 페이지 노출 확인' + bcolors.ENDC)

  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[2]/div[2]/button/span').click()

  #카테고리 등록 페이지 URL 확인
  print('카테고리 등록 페이지 이동 확인: {}'.format('정상' if DISPLAY_CATEGORY_ADD_URL == driver.current_url else '에러'))

  #카테고리 등록 페이지 타이틀 노출 확인
  title = driver.find_element(By.XPATH, '//*[@id="content"]/div/header/div/h2').text
  print('카테고리 등록 페이지 타이틀 확인: {}'.format('정상' if CATEGOTY_ADD_TITLE == title else '에러'))


def ATC_04_WirteListingCategoryField():
  print(bcolors.HEADER + 'ATC_04_전시 카테고리 등록 페이지 필드 입력 확인' + bcolors.ENDC)
  #전시 카테고리명 입력 
  driver.find_element(By.XPATH,'//*[@id="content"]/div/div[1]/div[2]/div[2]/div/input').send_keys(SAMPLE_ADDCATEGORY_NAME)

  #전시 상태 버튼 선택
  #1. 전시중
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div[2]/span[1]/label').click()
  time.sleep(1)

  #2. 전시중지
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div[2]/span[2]/label').click()
  time.sleep(1)

  #정렬 옵션 버튼 선택
  #1. 인기도순/새상품/가격 낮은 순/가격 높은 순
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[4]/div[2]/span[1]/label').click()
  time.sleep(1)

  #2. 새상품순
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[4]/div[2]/span[2]/label').click()
  time.sleep(1)

  #3. 가격 낮은 순
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[4]/div[2]/span[3]/label').click()
  time.sleep(1)

  #4. 가격 높은 순 
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[4]/div[2]/span[4]/label').click()
  time.sleep(1)

  #전시 순서 선택 (0~9999) 
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div[2]/div[1]').click()
  time.sleep(1)

  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div[2]/div[2]/div/span[2]').click()
  time.sleep(1)

  #[상품 등록] 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[2]/button').click()

  #전시 카테고리 등록 상품 추가
  #드롭다운 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div/div[1]/div[1]/div[1]/div/div').click()
  #카테고리 선택
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div[2]/div/div[1]/div/div/ul[1]/li[1]/label').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div[2]/div/div[1]/div/div/ul[2]/li/label').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div[2]/div/div[1]/div/div/ul[3]/li/label').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div[2]/div/div[2]/div/button[2]/span').click()

  #상품 선택
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div/div[1]/div[3]/table/tbody/tr[1]/td[1]/span/label').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div/div[2]/div/button[2]/span').click()

  #저장버튼 클릭 후, 얼럿 확인
  ###
  ###

def ATC_05_AddListingCategoryCheck():
  print(bcolors.HEADER + 'ATC_05_전시 카테고리 등록 확인' + bcolors.ENDC)

def ATC_06_FindEditListingCategory():
  print(bcolors.HEADER + 'ATC_06_전시 카테고리 수정 페이지 노출 확인' + bcolors.ENDC)

  # 검색어 입력 후 검색 버튼 클릭
  driver.find_element(By.CLASS_NAME,'input_text').send_keys(SAMPLE_CATEGORY_NAME)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[3]/button[1]').click()

  #1. [수정] 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[3]/table/tbody/tr/td[5]/button').click()

  #카테고리 등록 페이지 URL 확인
  print('카테고리 수정 페이지 이동 확인: {}'.format('정상' if DISPLAY_CATEGORY_EDIT_URL == driver.current_url else '에러'))

  #카테고리 수정 페이지 타이틀 노출 확인
  title = driver.find_element(By.XPATH, '//*[@id="content"]/div/header/div/h2').text
  print('카테고리 수정 페이지 타이틀 확인: {}'.format('정상' if CATEGOTY_EDIT_TITLE == title else '에러'))

def ATC_07_ModifyListingCategoryField():
  print(bcolors.HEADER + 'ATC_07_전시 카테고리 수정 페이지 필드 입력 확인' + bcolors.ENDC)

  #전시 카테고리명 초기화
  driver.find_element(By.XPATH,'//*[@id="content"]/div/div[1]/div[2]/div[2]/div/input').clear()

  #전시 카테고리명 입력 
  driver.find_element(By.XPATH,'//*[@id="content"]/div/div[1]/div[2]/div[2]/div/input').send_keys(SAMPLE_EDITCATEGORY_NAME)

  #전시 상태 버튼 선택
  #1. 전시중
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div[2]/span[1]/label').click()
  time.sleep(1)

  #2. 전시중지
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div[2]/span[2]/label').click()
  time.sleep(1)

  #정렬 옵션 버튼 선택
  #1. 인기도순
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[4]/div[2]/span[1]/label').click()
  time.sleep(1)

  #2. 새상품순
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[4]/div[2]/span[2]/label').click()
  time.sleep(1)

  #3. 가격 낮은 순
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[4]/div[2]/span[3]/label').click()
  time.sleep(1)

  #4. 가격 높은 순 
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[4]/div[2]/span[4]/label').click()
  time.sleep(1)

  #전시 순서 선택 (0~9999) 
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div[2]/div[1]').click()
  time.sleep(1)

  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div[2]/div[2]/div/span[2]').click()
  time.sleep(1)

  #[상품 등록] 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[1]/div[2]/button').click()

  #전시 카테고리 등록 상품 추가
  #드롭다운 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div/div[1]/div[1]/div[1]/div/div').click()
  #카테고리 선택
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div[2]/div/div[1]/div/div/ul[1]/li[1]/label').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div[2]/div/div[1]/div/div/ul[2]/li/label').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div[2]/div/div[1]/div/div/ul[3]/li/label').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div[2]/div/div[2]/div/button[2]/span').click()

  #상품 선택
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div/div[1]/div[3]/table/tbody/tr[1]/td[1]/span/label').click()
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[4]/div/div[2]/div/button[2]/span').click()

  #수정 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/button[2]/span').click()

  #얼럿 확인
  try:
    WebDriverWait(driver, 3).until(EC.alert_is_present())
    confirm_alert = driver.switch_to.alert
    print("얼럿 문구 확인 : " + confirm_alert.text)
    
    confirm_alert.accept()

  except:
    print("no alert")
    time.sleep(3)


def ATC_08_EditListingCategoryCheck():
    print(bcolors.HEADER + 'ATC_08_전시 카테고리 등록 확인' + bcolors.ENDC)


def ATC_09_RestListingCategory():
  print(bcolors.HEADER + '(((ATC_09_전시 카테고리 수정 템플릿 리셋)))' + bcolors.ENDC)

  # 검색어 입력 후 검색 버튼 클릭
  driver.find_element(By.CLASS_NAME,'input_text').send_keys(SAMPLE_EDITCATEGORY_NAME)
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[1]/div/div[3]/button[1]').click()

  #[수정] 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="@743qocoj"]/div[2]/div[1]/div[3]/table/tbody/tr/td[5]/button').click()

  #전시 카테고리명 초기화
  driver.find_element(By.XPATH,'//*[@id="content"]/div/div[1]/div[2]/div[2]/div/input').clear()
  time.sleep(1)

  #전시 카테고리명 입력 
  driver.find_element(By.XPATH,'//*[@id="content"]/div/div[1]/div[2]/div[2]/div/input').send_keys(SAMPLE_CATEGORY_NAME)

  #전시 상태 버튼 선택
  #1. 전시중
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[3]/div[2]/span[1]/label').click()
  time.sleep(1)

  #정렬 옵션 버튼 선택
  #1. 인기도순
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[4]/div[2]/span[1]/label').click()
  time.sleep(1)

  #전시 순서 선택 (0~9999) 
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div[2]/div[1]').click()
  time.sleep(1)

  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[5]/div[2]/div[2]/div/span[1]').click()
  time.sleep(1)

  #상품 삭제
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[2]/table/tbody/tr[1]/td[6]/button').click()

  #수정 버튼 클릭
  driver.find_element(By.XPATH, '//*[@id="content"]/div/div[3]/div/button[2]/span').click()

  #얼럿 확인
  try:
    WebDriverWait(driver, 3).until(EC.alert_is_present())
    confirm_alert = driver.switch_to.alert
    print("얼럿 문구 확인 : " + confirm_alert.text)
    
    confirm_alert.accept()

  except:
    print("no alert")
    time.sleep(3)


init()
login()
#ATC_01_ListingCategorySearchCheck()
#ATC_02_ListingCategoryResultsCheck()
#ATC_03_FindAddListingCategory()
#ATC_04_WirteListingCategoryField()
#ATC_05_AddListingCategoryCheck()
ATC_06_FindEditListingCategory()
ATC_07_ModifyListingCategoryField()
#ATC_08_EditListingCategoryCheck()
ATC_09_RestListingCategory()