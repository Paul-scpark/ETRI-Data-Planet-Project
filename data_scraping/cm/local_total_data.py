# library setting ----------------------------------------------------------------
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# url : 데이터받기 페이지  ----------------------------------------------------------------

data_get_url = "https://www.localdata.go.kr/devcenter/dataDown.do?menuNo=20001"

# list setting ----------------------------------------------------------------

total_data_df = []
total_format_list = []
total_download_list = []
total_script_list = []
total_format_list = []

life_good_df = []
life_name_list = []
life_download_list = []
life_label_list = []
life_script_list = []
names = ['전체분', '전체분', '전체분', '변동분', '변동분', '변동분', '일일분', '일일분', '일일분']


with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver :
    driver.get(data_get_url)

    # 전체 데이터 다운로드 페이지 전환
    driver.find_element(By.XPATH, "//*[@id='down-area']/div[1]").click()

    # 대상 지정
    download_link = driver.find_elements(By.CSS_SELECTOR, f"div.total-down a")
    scripts = driver.find_elements(By.CSS_SELECTOR, f"div.total-down p:nth-child(5)")

    # 데이터 추출
    for link in download_link :
        total_format_list.append(link.text)
        total_download_list.append(link.get_attribute('href'))

    for script in scripts :
        total_script_list += script.text.replace('\n', ',').replace('   ', ',').replace('  ','').split(',') * 3


total_data_df = pd.DataFrame({"label" : "인허가 데이터", "이름": names, "설명":total_script_list,
                                "파일 제공 형식" : total_format_list, "다운로드": total_download_list})




# 전국 무인민원발급기 & 전국 모범음식점 페이지 ----------------------------------------------------------------

muin_mobum_url = "https://www.localdata.go.kr/lif/lifeMainInfo.do?menuNo=40001"
mobum_info_url = "https://www.localdata.go.kr/portal/portalLifeInfo.do?menuNo=30003"

# 전국 무인민원발급기 스크래핑 -----
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver : 
    driver.get(muin_mobum_url)
    driver.implicitly_wait(10)

    labels = driver.find_elements(By.CSS_SELECTOR, f"div.content-title")
    download_link = driver.find_elements(By.CSS_SELECTOR, f"p.total-dataDown-btn a")
    titles = driver.find_elements(By.CSS_SELECTOR, f"div.info-title")

    for label in labels :
        life_label_list.append(label.text)

    for link in download_link :
        life_download_list.append(link.get_attribute('href'))

    for title in titles :
        life_name_list +=title.text.replace('/', ',').split(',')


# 전국 모범음식점 스크래핑 -----
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver : 

    driver.get(mobum_info_url)
    driver.implicitly_wait(10)
    scripts = driver.find_elements(By.CSS_SELECTOR, f"div.kind-info")

    for script in scripts:
        life_script_list.append(script.text.replace('\n', ' ').replace('·', ''))


life_good_df = pd.DataFrame({"label" : life_label_list[0], "이름": life_name_list, "설명" : life_script_list,
                              "파일 제공 형식" : 'EXCEL', "다운로드": life_download_list})


# result dataframe concat ----------------------------------------------------------------

result = pd.concat([total_data_df, life_good_df])
result.to_csv("./localdata(total_data).csv", encoding="utf-8")
