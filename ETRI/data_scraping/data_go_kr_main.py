# -*- coding: utf-8 -*-
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup, NavigableString, Tag
import csv, time, json, requests, multiprocessing, argparse, os.path, warnings

warnings.filterwarnings("ignore")


def get_href(URL, href_lst):
    response = requests.get(URL)
    soups = BeautifulSoup(response.text, "html.parser")

    for li in soups.select("#fileDataList > div.result-list > ul > li"):
        href_lst.append(li.select_one("dl > dt > a")["href"])


def get_data(URL):
    response = requests.get("https://www.data.go.kr" + URL)
    soups = BeautifulSoup(response.text, "html.parser")

    section_lst = soups.select(
        "#tab-layer-openapi > .api-meta-table-mobile > table > tr"
    )
    if len(section_lst) == 0:
        section_lst = soups.select(
            "#data-search-view > #file-meta-table-pc > table > tr"
        )

    section_dic = {}
    for section in section_lst:
        section_dic[section.select_one("th").text] = section.select_one("td").text

    if len(section_dic.keys()) > 0:
        section_dic["url"] = "https://www.data.go.kr" + URL

        with open("data_go_kr_data.csv", "a", newline="") as csvfile:
            fieldnames = list(section_dic.keys())
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                csv_writer.writeheader()
            csv_writer.writerow(section_dic)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_point", type=int, default=0)
    parser.add_argument("--end_point", type=int, default=500)
    args = parser.parse_args()
    print("args: ", args)

    manager1 = multiprocessing.Manager()
    href_lst = manager1.list()
    jobs1 = []
    ### 공공데이터 포털 홈페이지 각 페이지 별로 존재하는 데이터 소스의 href 주소를 href_lst에 append
    ## 데이터의 양이 많기 때문에 1번에 1개씩 처리하는게 아닌, multiprocessing을 이용하여 병렬로 다수의 jobs을 처리
    for i in tqdm(range(1, 1380)):
        URL = f"""https://www.data.go.kr/tcs/dss/selectDataSetList.do?
            dType=FILE&keyword=&detailKeyword=&publicDataPk=&recmSe=&detailText=&relatedKeyword=&commaNotInData
            =&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=updtDt&relRadio
            =&orgFullName=&orgFilter=&org=&orgSearch=&currentPage={i}&perPage=40&brm=&instt=&svcType
            =&kwrdArray=&extsn=&coreDataNmArray=&pblonsipScopeCode=
            """

        p = multiprocessing.Process(target=get_href, args=(URL, href_lst))
        jobs1.append(p)
        p.start()

    for proc in jobs1:
        proc.join()

    manager2 = multiprocessing.Manager()
    jobs2 = []
    ### 위에서 수집한 href_lst 각각에 접근하여 세부 데이터 가져와서 data_go_kr_data.csv 파일로 append 하여 저장
    ## 이때도 위와 동일하게 multiprocessing을 이용하여 병렬 처리로 속도를 개선
    for URL in tqdm(href_lst[args.start_point : args.end_point]):
        p = multiprocessing.Process(target=get_data, args=(URL,))
        jobs2.append(p)
        p.start()

    for proc in jobs2:
        proc.join()
