from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

url = "https://www.data.go.kr/tcs/dss/selectDataSetList.do?" \
      "dType=FILE&keyword=&detailKeyword=&publicDataPk=&recmSe=&detailText=" \
      "&relatedKeyword=&commaNotInData=&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=updtDt" \
      "&relRadio=&orgFullName=&orgFilter=&org=&orgSearch=&currentPage=1&perPage=10&brm=&instt=&svcType=&kwrdArray=&extsn=&coreDataNmArray=&pblonsipScopeCode="
options = webdriver.ChromeOptions()
# 탭 간 이동 활성화
options.add_argument("no-sandbox")
# options.add_argument("headless")

label_list = []
link_list = []
form_list = []
name_list = []
script_list = []
provider_list = []
date_list = []
view_list = []
download_list = []
keyword_list = []

with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
    driver.get(url)
    driver.implicitly_wait(5)

    page_num = 1
    while page_num <= 1000:
        driver.implicitly_wait(5)
        for content_num in range(1, 11):

            labels = driver.find_elements(By.CSS_SELECTOR, f"div.result-list li:nth-child({content_num}) p.tag-area")
            links = driver.find_elements(By.CSS_SELECTOR, f"div.result-list li:nth-child({content_num}) dl a")
            forms = driver.find_elements(By.CSS_SELECTOR, f"div.result-list li:nth-child({content_num}) dl a span.tagset")
            names = driver.find_elements(By.CSS_SELECTOR, f"div.result-list li:nth-child({content_num}) dl a span.title")
            scripts = driver.find_elements(By.CSS_SELECTOR, f"div.result-list li:nth-child({content_num}) dl dd")
            providers = driver.find_elements(By.CSS_SELECTOR,
                                             f"div.result-list li:nth-child({content_num}) div.info-data p:first-child span.data")
            dates = driver.find_elements(By.CSS_SELECTOR, f"div.result-list li:nth-child({content_num}) div.info-data p:nth-child(2) span.data")
            views = driver.find_elements(By.CSS_SELECTOR, f"div.result-list li:nth-child({content_num}) div.info-data p:nth-child(3) span.data")
            downloads = driver.find_elements(By.CSS_SELECTOR,
                                             f"div.result-list li:nth-child({content_num}) div.info-data p:nth-child(4) span.data")
            keywords = driver.find_elements(By.CSS_SELECTOR, f"div.result-list li:nth-child({content_num}) div.info-data p:last-child")

            for label in labels:
                label_list.append(label.text)

            for link in links:
                link_list.append(link.get_attribute('href'))

            temp_form_list = []
            for form in forms:
                temp_form_list.append(form.text)
                temp_form = " ".join(temp_form_list)
            form_list.append(temp_form)

            for name in names:
                name_list.append(name.text)

            for script in scripts:
                script_list.append(script.text)

            for provider in providers:
                provider_list.append(provider.text)

            for date in dates:
                date_list.append(date.text)

            for view in views:
                view_list.append(view.text)

            for download in downloads:
                download_list.append(download.text)

            for keyword in keywords:
                keyword_list.append(keyword.text[4:])

        page_num += 1
        time.sleep(1)
        driver.execute_script(f'updatePage({page_num}); return false;')

        time.sleep(1)

    df = pd.DataFrame({"분류체계": label_list,
                       "URL": link_list,
                       "제공형식": form_list,
                       "이름": name_list,
                       "명세": script_list,
                       "제공기관": provider_list,
                       "수정일": date_list,
                       "조회수": view_list,
                       "다운로드": download_list,
                       "키워드": keyword_list
                       })

    df.to_csv("./result.csv", encoding="utf-8")
