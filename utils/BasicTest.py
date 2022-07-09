import bs4
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import os
import configs.config as config

class BasicTest:
  base_url = config.OKKY_URL

  # 엘리먼트 기다리기
  def _wait(self, driver, by: str = By.ID, el = ''):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, el)))

  # 드라이버 이동 후 기다릴 대상 선택
  def _move(self, driver, resource: str, by: str = By.ID, el = ''):
    driver.get(f'{self.base_url}{resource}')
    return self._wait(driver, by, el)

  # 대상 찾기
  def _find(self, driver, by: str = By.ID, el = ''):
    return driver.find_element(by, el)

  # page 파싱하기
  def _bs(self, driver):
    return BeautifulSoup(driver.page_source, 'html.parser')

  def _bs_table(self, bs, selector):
    values = []
    columns
    table = bs.select_one(selector)
    tbody = table.find('tbody')
    trs = tbody.find_all('tr')

    for idx, tr in trs:
      tds = tr.find_all('td')
      tds = [td.text.strip() for td in tds]
      row = [cell for cell in tds if cell]
      if idx == 1:
        columns = row
      else:
        values.append(row)

    return pd.DataFrame(values, columns=columns)
  # def _screenshot(self, driver, file_name, sub_name):
  #   driver.save_screenshot(f'{os.path.realpath(__file__)}../{file_name}-{sub_name}.png')