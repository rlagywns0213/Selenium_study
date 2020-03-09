# reply_crawling/reply_crawling.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
import time
from PIL import Image
from io import BytesIO  # 바이트 형태로 저장해서(특수한 경우)

keyword = '국립'

url = "https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=015&aid=0004302944"

# 드라이버 연결 인스턴스
driver = webdriver.Chrome('../driver/chromedriver')
driver.implicitly_wait(1)
driver.maximize_window()

# 페이지 이동
print("[접속하기]")
driver.get(url)

##더보기 버튼 누르기
print("[더보기 클릭 중]")
attempt = 0
driver.find_element_by_css_selector('span.u_cbox_in_view_comment').click()
while True:
    try:
        driver.find_element_by_css_selector('span.u_cbox_page_more').click()
        attempt = 0  # 찾으면 시도횟수를 0으로 초기화
    except:
        attempt += 1
        if attempt > 5:
            break  # 더이상 더보기 버튼이 없다고 생각하겠다.
##댓글 요소 찾기
print("[댓글 요소 찾기]")
replys = driver.find_elements_by_css_selector('ul.u_cbox_list > li.u_cbox_comment')
print(len(replys))

# 작성자 : span.u_cbox_name ,  댓글내용 : span.u_cbox_contents
##작성자와 댓글 내용 추출 ( 작성자, 댓글내용)
print("[댓글 내용 수집]")
results = []
keyword_results = []  # (index, author, content)
del_msg = 0
for index, reply in enumerate(replys):
    try:
        author = reply.find_element_by_css_selector('span.u_cbox_name').text
        content = reply.find_element_by_css_selector('span.u_cbox_contents').text
        results.append((author, content))

        # 키워드가 있는지 확인
        if keyword in content:
            keyword_results.append((index, author, content))
    except:
        del_msg += 1  # 삭제된 댓글 카운트

print("삭제된 댓글 개수 :", del_msg)
pprint(results)

##폴더 생성
print("[폴더 생성]")
import os

folder_name = keyword
if not os.path.isdir('./{}'.format(folder_name)):
    os.mkdir('./{}'.format(folder_name))

## 상단바 삭제
print("[상단바 메뉴 숨기기")
header = driver.find_element_by_css_selector('#header')
driver.execute_script("arguments[0].style.display = 'none'", header)

# ##캡쳐하기 -1
# for index, k in enumerate(keyword_results):
#     replys[k[0]].screenshot('./{0}/{0}{1}.png'.format(keyword,index))

##캡쳐하기 -2

print(['캡쳐 시작'])
for index, k in enumerate(keyword_results):
    # 해당 요소까지 스크롤
    driver.execute_script("arguments[0].scrollIntoView(true);", replys[k[0]])

    # 현재 화면 캡쳐
    img = driver.get_screenshot_as_png()  # 바이너리 형태로 저장

    ##요소 좌표를 추출하고 -> '현재 화면 캡쳐사진'에서 잘라내고 저장하기
    location = replys[k[0]].location_once_scrolled_into_view  # 현재 화면에서 해당 요소가 어디 있는지 dict형태 반환
    size = replys[k[0]].size

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    box = (left, top, right, bottom)

    if location:
        im = Image.open(BytesIO(img))  # Image.open()에 바이너리 형태를 바로 넣으려면 ByteIO가 필요
        im = im.crop(box)
        im.save('./{0}/{0}{1}.png'.format(keyword, index))

##엑셀 파일 만들기 pandas  openpyxl
print("[전체 댓글 엑셀로 저장")
import pandas as pd

col = ["작성자", "내용"]
data_frame = pd.DataFrame(results, columns=col)
data_frame.to_excel('엑셀파일명.xlsx', sheet_name='수집시트명', startrow=0, header=True)

# 닫아주기
time.sleep(3)
driver.quit()
