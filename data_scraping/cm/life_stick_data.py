# library setting -----------------------------------------------------------------------------------------------------------------------------

import numpy as np
import pandas as pd
import requests 
from bs4 import BeautifulSoup 
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# 1 공중 화장실 정보 크롤링 -----------------------------------------------------------------------------------------------------------------------------

공중_화장실_컬럼명, 번호, 화장실명, 주소 , 개방시간, 관리기관명, 데이터기준일자 = [], [], [], [], [], [], []
life_stick_url = "https://www.localdata.go.kr/lif/lifeCtacDataView.do?menuNo=40003"

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(life_stick_url)
    driver.implicitly_wait(2)
            
    cols = driver.find_elements(By.CSS_SELECTOR, f"#etc-data-table table thead th")
    for col in cols :
        공중_화장실_컬럼명.append(col.text)

    # 마지막 페이지 넘버 추출
    last_page_number = driver.find_elements(By.CSS_SELECTOR, f"#navigator > a:nth-child(13)")
    for number in last_page_number :
        num = number.get_attribute('href')
        lpn = re.sub(r'[^0-9]', '', num)

    for i in range(1, lpn+1):
        driver.execute_script("goPage({})".format(i))
        driver.implicitly_wait(2)

        for i in range(1, 31):
            cols1 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td.chooseData.text-center".format(i))
            cols2 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(2)".format(i))
            cols3 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(3)".format(i))
            cols4 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(4)".format(i))
            cols5 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(5)".format(i))
            cols6 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(6)".format(i))
            
            for col1 in cols1 : 번호.append(col1.text) 
            for col2 in cols2 : 화장실명.append(col2.text)
            for col3 in cols3 : 주소.append(col3.text)
            for col4 in cols4 : 개방시간.append(col4.text)
            for col5 in cols5 : 관리기관명.append(col2.text)
            for col6 in cols6 : 데이터기준일자.append(col6.text)

공중_화장실_정보 = pd.DataFrame(zip(번호, 화장실명, 주소 , 개방시간, 관리기관명, 데이터기준일자), columns=공중_화장실_컬럼명)

# 2. 보호수 정보 크롤링 -----------------------------------------------------------------------------------------------------------------------------
보호수_컬럼명, 번호, 지정번호, 주소 , 보호수지정일자, 관리기관명, 데이터기준일자 = [], [], [], [], [], [], []
life_stick_url = "https://www.localdata.go.kr/lif/lifeCtacDataView.do?menuNo=40003"


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(life_stick_url)
    driver.find_element(By.XPATH, "//*[@id='opnLeftList']/li[2]/a").click()
    driver.implicitly_wait(2)

    cols = driver.find_elements(By.CSS_SELECTOR, f"#etc-data-table table thead th")
    for col in cols :
        보호수_컬럼명.append(col.text)

    for i in range(1, 10):
        driver.execute_script("goPage({})".format(i))
        driver.implicitly_wait(2)
        
        for i in range(1, 31):
                cols1 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td.chooseData.text-center".format(i))
                cols2 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(2)".format(i))
                cols3 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(3)".format(i))
                cols4 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(4)".format(i))
                cols5 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(5)".format(i))
                cols6 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(6)".format(i))
                for col1 in cols1 : 
                    번호.append(col1.text)
                for col2 in cols2 : 
                    지정번호.append(col2.text)
                for col3 in cols3 : 
                    주소.append(col3.text)
                for col4 in cols4 : 
                    보호수지정일자.append(col4.text)
                for col5 in cols5 : 
                    관리기관명.append(col2.text)
                for col6 in cols6 : 
                    데이터기준일자.append(col6.text)
보호수_정보 = pd.DataFrame(zip(번호, 지정번호, 주소 , 보호수지정일자, 관리기관명, 데이터기준일자), columns=보호수_컬럼명)


# 3. 자전거 보관소 정보 크롤링 -----------------------------------------------------------------------------------------------------------------------------
자전거_보관소_컬럼명, 번호, 자전거보관소명, 주소 , 보관대수, 관리기관명, 데이터기준일자 = [], [], [], [], [], [], []
life_stick_url = "https://www.localdata.go.kr/lif/lifeCtacDataView.do?menuNo=40003"

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(life_stick_url)
    driver.find_element(By.XPATH, "//*[@id='opnLeftList']/li[3]/a").click()
    driver.implicitly_wait(2)

    cols = driver.find_elements(By.CSS_SELECTOR, f"#etc-data-table table thead th")
    for col in cols :
        자전거_보관소_컬럼명.append(col.text)

    # 마지막 페이지 넘버 추출
    last_page_number = driver.find_elements(By.CSS_SELECTOR, f"#navigator > a:nth-child(13)")
    for number in last_page_number :
        num = number.get_attribute('href')
        lpn = re.sub(r'[^0-9]', '', num)

    for i in range(1, lpn+1):
        driver.execute_script("goPage({})".format(i))
        driver.implicitly_wait(2)
        
        for i in range(1, 31):
                cols1 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td.chooseData.text-center".format(i))
                cols2 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(2)".format(i))
                cols3 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(3)".format(i))
                cols4 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(4)".format(i))
                cols5 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(5)".format(i))
                cols6 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(6)".format(i))
                for col1 in cols1 :    
                    번호.append(col1.text)
                for col2 in cols2 : 
                    자전거보관소명.append(col2.text)
                for col3 in cols3 : 
                    주소.append(col3.text)
                for col4 in cols4 : 
                    보관대수.append(col4.text)
                for col5 in cols5 : 
                    관리기관명.append(col2.text)
                for col6 in cols6 : 
                    데이터기준일자.append(col6.text)
자전거_보관소_정보 = pd.DataFrame(zip(번호, 자전거보관소명, 주소 , 보관대수, 관리기관명, 데이터기준일자), columns=자전거_보관소_컬럼명)


# 4. 생활쓰레기배출정보 크롤링 -----------------------------------------------------------------------------------------------------------------------------
생활쓰레기배출정보_컬럼명, 번호, 관리구역명, 배출장소 , 미수거일, 관리부서명, 데이터기준일자 = [], [], [], [], [], [], []
life_stick_url = "https://www.localdata.go.kr/lif/lifeCtacDataView.do?menuNo=40003"


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(life_stick_url)
    driver.find_element(By.XPATH, "//*[@id='opnLeftList']/li[4]/a").click()
    driver.implicitly_wait(2)

    cols = driver.find_elements(By.CSS_SELECTOR, f"#etc-data-table table thead th")
    for col in cols :
        생활쓰레기배출정보_컬럼명.append(col.text)

    for i in range(1, 4):
        driver.execute_script("goPage({})".format(i))
        driver.implicitly_wait(2)
        
        for i in range(1, 31):
                cols1 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td.chooseData.text-center".format(i))
                cols2 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(2)".format(i))
                cols3 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(3)".format(i))
                cols4 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(4)".format(i))
                cols5 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(5)".format(i))
                cols6 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(6)".format(i))
                for col1 in cols1 :    
                    번호.append(col1.text)
                for col2 in cols2 : 
                    관리구역명.append(col2.text)
                for col3 in cols3 : 
                    배출장소.append(col3.text)
                for col4 in cols4 : 
                    미수거일.append(col4.text)
                for col5 in cols5 : 
                    관리부서명.append(col2.text)
                for col6 in cols6 : 
                    데이터기준일자.append(col6.text)
생활쓰레기배출_정보 = pd.DataFrame(zip(번호, 관리구역명, 배출장소 , 미수거일, 관리부서명, 데이터기준일자), columns=생활쓰레기배출정보_컬럼명)

# 5. 세차장정보 크롤링 -----------------------------------------------------------------------------------------------------------------------------
세차장정보_컬럼명, 번호, 사업장명, 주소, 사업장업종명, 휴무일, 데이터기준일 = [], [], [], [], [], [], []
life_stick_url = "https://www.localdata.go.kr/lif/lifeCtacDataView.do?menuNo=40003"


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(life_stick_url)
    driver.find_element(By.XPATH, "//*[@id='opnLeftList']/li[5]/a").click()
    driver.implicitly_wait(2)

    cols = driver.find_elements(By.CSS_SELECTOR, f"#etc-data-table table thead th")
    for col in cols :
        세차장정보_컬럼명.append(col.text)

    # 마지막 페이지 넘버 추출
    last_page_number = driver.find_elements(By.CSS_SELECTOR, f"#navigator > a:nth-child(13)")
    for number in last_page_number :
        num = number.get_attribute('href')
        lpn = re.sub(r'[^0-9]', '', num)

    for i in range(1, lpn+1):
        driver.execute_script("goPage({})".format(i))
        driver.implicitly_wait(2)
        
        for i in range(1, 31):
                cols1 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td.chooseData.text-center".format(i))
                cols2 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(2)".format(i))
                cols3 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(3)".format(i))
                cols4 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(4)".format(i))
                cols5 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(5)".format(i))
                cols6 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(6)".format(i))
                for col1 in cols1 :    
                    번호.append(col1.text)
                for col2 in cols2 : 
                    사업장명.append(col2.text)
                for col3 in cols3 : 
                    주소.append(col3.text)
                for col4 in cols4 : 
                    사업장업종명.append(col4.text)
                for col5 in cols5 : 
                    휴무일.append(col2.text)
                for col6 in cols6 : 
                    데이터기준일.append(col6.text)


세차장_정보 = pd.DataFrame(zip(번호, 사업장명, 주소, 사업장업종명, 휴무일, 데이터기준일), columns=세차장정보_컬럼명)


# 6. 과속방지턱정보 크롤링 -----------------------------------------------------------------------------------------------------------------------------
과속방지턱정보_컬럼명, 번호, 과속방지턱형태구분, 주소, 과속방지턱재료,	관리기관명,	데이터기준일자 = [], [], [], [], [], [], []
life_stick_url = "https://www.localdata.go.kr/lif/lifeCtacDataView.do?menuNo=40003"


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(life_stick_url)
    driver.find_element(By.XPATH, "//*[@id='opnLeftList']/li[6]/a").click()
    driver.implicitly_wait(2)

    cols = driver.find_elements(By.CSS_SELECTOR, f"#etc-data-table table thead th")
    for col in cols :
        과속방지턱정보_컬럼명.append(col.text)

    # 마지막 페이지 넘버 추출
    last_page_number = driver.find_elements(By.CSS_SELECTOR, f"#navigator > a:nth-child(13)")
    for number in last_page_number :
        num = number.get_attribute('href')
        lpn = re.sub(r'[^0-9]', '', num)

    for i in range(1, 954):
        driver.execute_script("goPage({})".format(i))
        driver.implicitly_wait(2)
        
        for i in range(1, 31):
                cols1 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td.chooseData.text-center".format(i))
                cols2 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(2)".format(i))
                cols3 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(3)".format(i))
                cols4 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(4)".format(i))
                cols5 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(5)".format(i))
                cols6 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(6)".format(i))
                for col1 in cols1 :    
                    번호.append(col1.text)
                for col2 in cols2 : 
                    과속방지턱형태구분.append(col2.text)
                for col3 in cols3 : 
                    주소.append(col3.text)
                for col4 in cols4 : 
                    과속방지턱재료.append(col4.text)
                for col5 in cols5 : 
                    관리기관명.append(col2.text)
                for col6 in cols6 : 
                    데이터기준일자.append(col6.text)

과속방지턱_정보 = pd.DataFrame(zip(번호, 과속방지턱형태구분, 주소, 과속방지턱재료,	관리기관명,	데이터기준일자), columns = 과속방지턱정보_컬럼명)


# 7. 무료와이파이정보 크롤링 -----------------------------------------------------------------------------------------------------------------------------
무료와이파이정보_컬럼명, 번호, 설치장소명, 주소, 설치시설구분,	관리기관명,	데이터기준일자 = [], [], [], [], [], [], []
life_stick_url = "https://www.localdata.go.kr/lif/lifeCtacDataView.do?menuNo=40003"


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(life_stick_url)
    driver.find_element(By.XPATH, "//*[@id='opnLeftList']/li[7]/a").click()
    driver.implicitly_wait(2)

    cols = driver.find_elements(By.CSS_SELECTOR, f"#etc-data-table table thead th")
    for col in cols :
        무료와이파이정보_컬럼명.append(col.text)

    # 마지막 페이지 넘버 추출
    last_page_number = driver.find_elements(By.CSS_SELECTOR, f"#navigator > a:nth-child(13)")
    for number in last_page_number :
        num = number.get_attribute('href')
        lpn = re.sub(r'[^0-9]', '', num) 
    
    for i in range(1, int(lpn)+1):
        driver.execute_script("goPage({})".format(i))
        driver.implicitly_wait(2)
        
        for i in range(1, 31):
                cols1 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td.chooseData.text-center".format(i))
                cols2 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(2)".format(i))
                cols3 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(3)".format(i))
                cols4 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(4)".format(i))
                cols5 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(5)".format(i))
                cols6 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(6)".format(i))
                for col1 in cols1 :    
                    번호.append(col1.text)
                for col2 in cols2 : 
                    설치장소명.append(col2.text)
                for col3 in cols3 : 
                    주소.append(col3.text)
                for col4 in cols4 : 
                    설치시설구분.append(col4.text)
                for col5 in cols5 : 
                    관리기관명.append(col2.text)
                for col6 in cols6 : 
                    데이터기준일자.append(col6.text)

무료와이파이_정보 = pd.DataFrame(zip(번호, 설치장소명, 주소, 설치시설구분,	관리기관명,	데이터기준일자), columns = 무료와이파이정보_컬럼명)

# 8. CCTV정보 크롤링 -----------------------------------------------------------------------------------------------------------------------------
CCTV정보_컬럼명, 번호, 설치목적구분, 주소, 설치연월, 관리기관명, 데이터기준일자 = [], [], [], [], [], [], []
life_stick_url = "https://www.localdata.go.kr/lif/lifeCtacDataView.do?menuNo=40003"


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(life_stick_url)
    driver.find_element(By.XPATH, "//*[@id='opnLeftList']/li[8]/a").click()
    driver.implicitly_wait(2)

    cols = driver.find_elements(By.CSS_SELECTOR, f"#etc-data-table table thead th")
    for col in cols :
        CCTV정보_컬럼명.append(col.text)

    # 마지막 페이지 넘버 추출
    last_page_number = driver.find_elements(By.CSS_SELECTOR, f"#navigator > a:nth-child(13)")
    for number in last_page_number :
        num = number.get_attribute('href')
        lpn = re.sub(r'[^0-9]', '', num)

    for i in range(1, int(lpn)+1):
        driver.execute_script("goPage({})".format(i))
        driver.implicitly_wait(2)
        
        for i in range(1, 31):
                cols1 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td.chooseData.text-center".format(i))
                cols2 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(2)".format(i))
                cols3 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(3)".format(i))
                cols4 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(4)".format(i))
                cols5 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(5)".format(i))
                cols6 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(6)".format(i))
                for col1 in cols1 :    
                    번호.append(col1.text)
                for col2 in cols2 : 
                    설치목적구분.append(col2.text)
                for col3 in cols3 : 
                    주소.append(col3.text)
                for col4 in cols4 : 
                    설치연월.append(col4.text)
                for col5 in cols5 : 
                    관리기관명.append(col2.text)
                for col6 in cols6 : 
                    데이터기준일자.append(col6.text)
CCTV_정보 = pd.DataFrame(zip(번호, 설치목적구분, 주소, 설치연월, 관리기관명, 데이터기준일자), columns = CCTV정보_컬럼명)

# 9. 안전비상벨위치정보 크롤링 -----------------------------------------------------------------------------------------------------------------------------
안전비상벨위치정보_컬럼명, 번호, 설치목적, 주소, 설치장소유형, 관리기관명, 데이터기준일자 = [], [], [], [], [], [], []
life_stick_url = "https://www.localdata.go.kr/lif/lifeCtacDataView.do?menuNo=40003"


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(life_stick_url)
    driver.find_element(By.XPATH, "//*[@id='opnLeftList']/li[9]/a").click()
    driver.implicitly_wait(2)

    cols = driver.find_elements(By.CSS_SELECTOR, f"#etc-data-table table thead th")
    for col in cols :
        안전비상벨위치정보_컬럼명.append(col.text)

    # 마지막 페이지 넘버 추출
    last_page_number = driver.find_elements(By.CSS_SELECTOR, f"#navigator > a:nth-child(13)")
    for number in last_page_number :
        num = number.get_attribute('href')
        lpn = re.sub(r'[^0-9]', '', num)

    for i in range(1, int(lpn)+1):
        driver.execute_script("goPage({})".format(i))
        driver.implicitly_wait(2)
        
        for i in range(1, 31):
                cols1 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td.chooseData.text-center".format(i))
                cols2 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(2)".format(i))
                cols3 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(3)".format(i))
                cols4 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(4)".format(i))
                cols5 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(5)".format(i))
                cols6 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(6)".format(i))
                for col1 in cols1 :    
                    번호.append(col1.text)
                for col2 in cols2 : 
                    설치목적.append(col2.text)
                for col3 in cols3 : 
                    주소.append(col3.text)
                for col4 in cols4 : 
                    설치장소유형.append(col4.text)
                for col5 in cols5 : 
                    관리기관명.append(col2.text)
                for col6 in cols6 : 
                    데이터기준일자.append(col6.text)

안전비상벨위치_정보 = pd.DataFrame(zip(번호, 설치목적, 주소, 설치장소유형, 관리기관명, 데이터기준일자), columns = 안전비상벨위치정보_컬럼명)


# 10. 낚시터정보 크롤링 -----------------------------------------------------------------------------------------------------------------------------
낚시터정보_컬럼명, 번호,낚시터명,주소,낚시터유형,관리기관명,데이터기준일자 = [], [], [], [], [], [], []
life_stick_url = "https://www.localdata.go.kr/lif/lifeCtacDataView.do?menuNo=40003"


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(life_stick_url)
    driver.find_element(By.XPATH, "//*[@id='opnLeftList']/li[10]/a").click()
    driver.implicitly_wait(2)

    cols = driver.find_elements(By.CSS_SELECTOR, f"#etc-data-table table thead th")
    for col in cols :
        낚시터정보_컬럼명.append(col.text)

       
    for i in range(1, 31):
            cols1 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td.chooseData.text-center".format(i))
            cols2 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(2)".format(i))
            cols3 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(3)".format(i))
            cols4 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(4)".format(i))
            cols5 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(5)".format(i))
            cols6 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(6)".format(i))
            for col1 in cols1 :    
                번호.append(col1.text)
            for col2 in cols2 : 
                낚시터명.append(col2.text)
            for col3 in cols3 : 
                주소.append(col3.text)
            for col4 in cols4 : 
                낚시터유형.append(col4.text)
            for col5 in cols5 : 
                관리기관명.append(col2.text)
            for col6 in cols6 : 
                데이터기준일자.append(col6.text)

낚시터_정보 = pd.DataFrame(zip(번호,낚시터명,주소,낚시터유형,관리기관명,데이터기준일자), columns = 낚시터정보_컬럼명)

# 11. 비산먼지발생사업정보 크롤링 -----------------------------------------------------------------------------------------------------------------------------
비산먼지발생사업정보_컬럼명, 번호, 사업자명, 주소, 관리기관명, 데이터기준일자 = [], [], [], [], [], [], []
life_stick_url = "https://www.localdata.go.kr/lif/lifeCtacDataView.do?menuNo=40003"


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(life_stick_url)
    driver.find_element(By.XPATH, "//*[@id='opnLeftList']/li[11]/a").click()
    driver.implicitly_wait(2)

    cols = driver.find_elements(By.CSS_SELECTOR, f"#etc-data-table table thead th")
    for col in cols :
        비산먼지발생사업정보_컬럼명.append(col.text)

    # 마지막 페이지 넘버 추출
    last_page_number = driver.find_elements(By.CSS_SELECTOR, f"#navigator > a:nth-child(13)")
    for number in last_page_number :
        num = number.get_attribute('href')
        lpn = re.sub(r'[^0-9]', '', num)

    for i in range(1, int(lpn)+1):
        driver.execute_script("goPage({})".format(i))
        driver.implicitly_wait(2)
        
        for i in range(1, 31):
                cols1 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td.chooseData.text-center".format(i))
                cols2 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(2)".format(i))
                cols3 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(3)".format(i))
                cols4 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(4)".format(i))
                cols5 = driver.find_elements(By.CSS_SELECTOR, "#etc-data-table > table > tbody > tr:nth-child({}) > td:nth-child(5)".format(i))
                for col1 in cols1 :    
                    번호.append(col1.text)
                for col2 in cols2 : 
                    사업자명.append(col2.text)
                for col3 in cols3 : 
                    주소.append(col3.text)
                for col4 in cols4 : 
                    관리기관명.append(col4.text)
                for col5 in cols5 : 
                    데이터기준일자.append(col2.text)

비산먼지발생사업_정보 = pd.DataFrame(zip(번호, 사업자명, 주소, 관리기관명, 데이터기준일자), columns = 비산먼지발생사업정보_컬럼명)


                    
공중_화장실_정보.to_csv("./공중_화장실_정보.csv", encoding="utf-8")
보호수_정보.to_csv("./보호수_정보.csv", encoding="utf-8")
자전거_보관소_정보.to_csv("./자전거_보관소_정보_정보.csv", encoding="utf-8")
생활쓰레기배출_정보.to_csv("./생활쓰레기배출_정보.csv", encoding="utf-8")
세차장_정보.to_csv("./세차장_정보.csv", encoding="utf-8")
과속방지턱_정보.to_csv("./과속방지턱_정보.csv", encoding="utf-8")
무료와이파이_정보.to_csv("./무료와이파이_정보.csv", encoding="utf-8")
CCTV_정보.to_csv("./CCTV_정보.csv", encoding="utf-8")
안전비상벨위치_정보.to_csv("./안전비상벨위치_정보.csv", encoding="utf-8")
비산먼지발생사업_정보.to_csv("./비산먼지발생사업_정보.csv", encoding="utf-8")
낚시터_정보.to_csv("./낚시터_정보.csv", encoding="utf-8")