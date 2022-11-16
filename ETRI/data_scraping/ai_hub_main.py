# -*- coding: utf-8 -*-
import csv, time, json, requests, warnings
from tqdm import tqdm
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings("ignore")


def get_json_using_bs4(URL, data):
    response = requests.post(URL, data)
    soups = BeautifulSoup(response.text, "html.parser")
    return json.loads(soups.text)


def get_soup_using_selenium(URL, driver):
    driver.get(URL)
    # 혹시 홈페이지 자체에서 alert이 있는 경우, 자동으로 accept하여 처리하기
    try:
        driver.switch_to.alert.accept()
    except:
        pass
    time.sleep(3)
    response = driver.page_source
    return BeautifulSoup(response, "html.parser")


def get_data_info(li):
    # 일자, 변경내용, 비고, 소개, 구축목적
    title = [li_h4.text for li_h4 in li.select("div > h4")]
    detail = [pre.text for pre in li.select("div > pre")]

    try:  # 페이지마다 조금 형식이 다른 부분이 있어서 try, except으로 예외처리 해주기
        table_selector = li.select("div > table")[1]
        tr_selector = table_selector.select_one("tbody > tr")
        table_col = [th.text for th in table_selector.select("thead > tr > th")]
        table_row = [span.text for span in tr_selector.select("td > span")]
    except:
        table_selector = li.select_one("div > table")
        table_col = [
            th.text for th in table_selector.select_one("thead > tr").select("th")
        ]
        table_row = [
            span.text
            for span in table_selector.select_one("tbody > tr").select("td > span")
        ]
        table_col, table_row = table_col[1:], table_row[1:]

    total_title = table_col + ["소개", "구축목적"]  # title에서 '소개'와 '구축목적'에 해당하는 것만 사용
    total_content = table_row + detail
    return dict(zip(total_title, total_content))


def get_data_structure(li):
    # 데이터 영역, 데이터 유형, 데이터 형식, 데이터 출처, 라벨링 유형, 라벨링 형식, 데이터 활용 서비스, 데이터 구축년도/데이터 구축량
    title_lst, detail_lst = [], []
    for tr in li.select("div > table > tbody > tr"):
        title_lst += [th.text for th in tr.select("th")]
        detail_lst += [
            li_td.text.replace("\t", "").replace("\n", "").replace("  ", "")
            for li_td in tr.select("td")
        ]
    return dict(zip(title_lst, detail_lst))


if __name__ == "__main__":
    data_lst = []
    ### AI HUB 홈페이지에 있는 각 데이터 소스 약 384개를 json 타입으로 하여 data_lst로 불러오기 (bs4 활용)
    ## 데이터 이름, 데이터셋 번호, 데이터 간략한 소개 등에 대한 정보를 담고 있음
    for page in tqdm(range(1, 21)):
        data = {
            "pageIndex": page,
            "currMenu": "115",
            "topMenu": "300",
            "dataSetSn": "",
            "srchdataClCode": "DATACL001",
            "srchOrder": "",
            "SrchdataClCode": "DATACL002",
            "searchKeyword": "",
        }
        soups_json = get_json_using_bs4(
            "https://www.aihub.or.kr/aihubdata/data/aJaxDataList.do", data
        )
        data_lst += [li for li in soups_json["list"]]

    ### 위에서 수집한 data_lst를 이용하여 각 데이터셋의 세부 페이지로 접근하여 정보 수집하기 (selenium 활용)
    ## 세부 페이지는 위에서 수집한 data_lst 안에 있는 'dataSetSn' 값을 이용하여 접근 할 수 있음
    for data_idx, i in enumerate(tqdm(data_lst)):
        with webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        ) as driver:
            URL = f"https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=300&aihubDataSe=realm&dataSetSn={i['dataSetSn']}"
            soups = get_soup_using_selenium(URL, driver)

            data_title = soups.select_one(
                "#content > div.tabDiv1 > div.dataHead > div > h3"
            ).text
            for idx, li in enumerate(
                soups.select("#content > div.tabDiv1 > div.contentWrap > ul > li")
            ):
                # AI HUB 홈페이지에서 '데이터 개요' 부분
                if idx == 0:
                    soup_sub1 = get_data_info(li)
                # AI HUB 홈페이지에서 '메타데이터 구조표' 부분
                elif idx == 1:
                    soup_sub2 = get_data_structure(li)

            soup_sub1.update(soup_sub2)
            soup_sub1["url"] = URL
            soup_sub1["title"] = data_title

            ### 각 페이지 별로 수집한 데이터들을 ai_hub_data.csv 파일로 append 하여 저장
            with open("ai_hub_data.csv", "a", newline="") as csvfile:
                fieldnames = list(soup_sub1.keys())
                csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if data_idx == 0:
                    csv_writer.writeheader()
                csv_writer.writerow(soup_sub1)

        time.sleep(3)
