from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

url = "https://data.seoul.go.kr/dataList/datasetList.do?datasetKind=1&searchFlag=M"
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
provider2_list = []
keyword_list = []

with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
    driver.get(url)
    driver.implicitly_wait(5)

    page_num = 1
    while page_num <= 2:
        driver.implicitly_wait(5)
        for content_num in range(1, 11):
            driver.implicitly_wait(5)
            labels = driver.find_elements(By.CSS_SELECTOR,
                                          f"div.list-statistics dl:nth-child({content_num}) dt em:nth-child(2)")
            links = driver.find_elements(By.CSS_SELECTOR, f"div.list-statistics dl:nth-child({content_num}) a")
            forms = driver.find_elements(By.CSS_SELECTOR,
                                         f"div.list-statistics dl:nth-child({content_num}) dd.list-statistics-info3 button")
            names = driver.find_elements(By.CSS_SELECTOR, f"div.list-statistics dl:nth-child({content_num}) a strong")
            providers = driver.find_elements(By.CSS_SELECTOR,
                                             f"div.list-statistics dl:nth-child({content_num}) dd.list-statistics-info2 span:nth-child(2)")
            dates = driver.find_elements(By.CSS_SELECTOR,
                                         f"div.list-statistics dl:nth-child({content_num}) dd.list-statistics-info2 span:nth-child(1)")
            providers2 = driver.find_elements(By.CSS_SELECTOR,
                                              f"div.list-statistics dl:nth-child({content_num}) dd.list-statistics-info2 span:nth-child(3)")

            for label in labels:
                temp_label = label.text[1:-1]
                label_list.append(temp_label)

            for link in links:
                temp_link = "https://data.seoul.go.kr/dataList/" + link.get_attribute('data-rel')
                link_list.append(temp_link)

            temp_form_list = []
            for form in forms:
                temp_form_list.append(form.text)
                temp_form = ",".join(temp_form_list)
            form_list.append(temp_form)

            for name in names:
                name_list.append(name.text)

            for provider in providers:
                temp_provider = provider.text.split(":")[-1].strip()
                provider_list.append(temp_provider)

            for date in dates:
                temp_date = date.text.split(":")[-1].strip()
                date_list.append(temp_date)

            for provider2 in providers2:
                temp_provider2 = provider2.text.split(":")[-1].strip()
                provider2_list.append(temp_provider2)

            driver.get(temp_link)
            driver.implicitly_wait(5)
            scripts = driver.find_elements(By.CSS_SELECTOR,
                                           "form#frm div.box-base.renewal div.main-content-renewal02 div.main-content-txt")
            for script in scripts:
                script_list.append(script.text)

            keywords = driver.find_elements(By.CSS_SELECTOR,
                                            f"form#frm div:nth-child(10) div.tbl-base-d.align-l.only-d2 table tbody tr:nth-child(8) td a")
            temp_keyword_list = []
            for keyword in keywords:
                temp_keyword_list.append(keyword.text)
                temp_keyword = ",".join(temp_keyword_list)
            keyword_list.append(temp_keyword)

            time.sleep(1)
            driver.back()
            time.sleep(1)

        page_num += 1
        time.sleep(1)
        driver.execute_script(f'fn_board_page({page_num}); return false;')

        time.sleep(1)

    df = pd.DataFrame({"카테고리": label_list,
                       "URL": link_list,
                       "제공형식": form_list,
                       "이름": name_list,
                       "명세": script_list,
                       "제공기관": provider_list,
                       "제공부서": provider2_list,
                       "수정일": date_list,
                       "관련 태그": keyword_list
                       })

    df.to_csv("./result3.csv", encoding="utf-8")
