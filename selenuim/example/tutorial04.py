# tutorial01.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('../driver/chromedriver.exe')
driver.implicitly_wait(3)

##페이지 이동
driver.get("http://www.naver.com")

## 검색창을 찾고 변수에 저장
search = driver.find_element_by_css_selector('#query')
search.send_keys('고슴도치')
#search.send_keys(Keys.ENTER)

btn =driver.find_element_by_css_selector('#search_btn')
btn.click()
time.sleep(3)
driver.quit()