# tutorial01.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url = "http://google.co.kr"

driver = webdriver.Chrome('../driver/chromedriver.exe')
driver.implicitly_wait(300) #묵시적 대기

#페이지 가져온다(이동)
driver.get(url)
time.sleep(5)
driver.quit()