# agent_crawling.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from tqdm import tqdm
import time

def get_agent_info_save(url=None, chrome_path ='./chromedriver', excel_name = '부동산중개사'):
        if not url:
            print("url은 필수입니다.")
            return False

        url = url
        driver = webdriver.Chrome(chrome_path)
        driver.implicitly_wait(1)

        #페이지 이동
        driver.get(url)

        ##정지 버튼 누르기
        driver.find_element_by_css_selector('a.btn_stop_on').click()

        ##몇 명인지 확인
        num = driver.find_element_by_css_selector('span.pagenum').text
        print(num) # 1/321
        num = int(num.split('/')[-1])
        print("인원 수:", num)


        ##해당 영역 찾기
        print("[정보 추출하기]")
        results = []
        for i in range(num):
            p_count = 0
            while True:
                if p_count > 3:
                    break
                try:
                    profile = driver.find_element_by_css_selector('div.bx_com')
                    data = {} #데이터 구성
                    ##업체명과 대표명, 가능 언어 추출
                    data['company'] = profile.find_element_by_css_selector('h5.t_mem').text
                    area1 = profile.find_element_by_css_selector('ul.lst_mem>li:nth-child(1)').text
                    data['name'] = area1.split('|')[0][len("대표 "):] #대표명

                    if '가능' in area1:
                        langs = area1.split  ('|')[1][:-3] #대표 반원|영어 가능 #영어, 영어일본어
                        #방법1 - 리스트나 튜플로 저장했을 때는?
                        #text = langs.split('어')
                        #data['lang'] = [x+'어' for x in text[:-1]]

                        #방법2
                        text = langs.split('어')[:-1]
                        for x in text:
                            data[x+'어'] = 'O'

                    area2 = profile.find_element_by_css_selector('ul.lst_mem>li:nth-child(2)').text
                    phones = area2[3:].split(' / ') # ['02-404-7750'] or ['02-404-7750','010-8939-1148']
                    for index , phone in enumerate(phones):
                        data['phone{}'.format(index+1)] = phone
                    results.append(data)
                    break
                except:
                    p_count+=1

            ## 맨 마지막 사람인지 확인 > 더보기 버튼 더이상 안누르게끔
            count = 0
            flag = False
            while True:
                if count > 3:
                    break
                try:
                    p_num = driver.find_element_by_css_selector('span.pagenum').text
                    p_num = int(p_num.split('/')[0])
                    #print("현재 탐색 번호:", p_num)
                    if num == p_num:
                        flag = True
                    break
                except:
                    count +=1
            if flag:
                break
            ##다음 프로필 보기
            count = 0
            while True:
                try:
                    profile.find_element_by_css_selector('a.btn_next_on').click()
                    #time.sleep(.5)
                    break
                except:
                    count +=1
                    if count> 3:
                        break


        ##엑셀 저장
        import pandas as pd
        print("[전체 댓글 엑셀로 저장]")
        #excel_name = "부동산 중개사"
        data_frame = pd.DataFrame(results)
        data_frame.to_excel('./{}.xlsx'.format(excel_name), sheet_name = excel_name, startrow=0, header = True)

        time.sleep(1)
        driver.quit()

#메인영역
if __name__ =='__main__':
    url = "https://land.naver.com/article/divisionInfo.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cortarNo=1171000000"
    get_agent_info_save(url, '../driver/chromedriver','송파구 중개사')