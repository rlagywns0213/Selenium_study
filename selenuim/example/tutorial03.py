# tutorial01.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('../driver/chromedriver.exe')
driver.implicitly_wait(3)

##페이지 가져오기
driver.get('http://www.google.co.kr')
driver.get('http://www.naver.com')
driver.get('http://www.youtube.com')

#이전 창 이동
driver.back()
time.sleep(.5)
driver.back()
time.sleep(.5)
#앞으로 이동
driver.forward()
time.sleep(.5)
driver.forward()
time.sleep(.5)

time.sleep(3)
driver.quit()