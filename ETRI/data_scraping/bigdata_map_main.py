# -*- coding: utf-8 -*-
from tqdm import tqdm
import pandas as pd
import time, json, requests, multiprocessing, warnings, os.path
from bs4 import BeautifulSoup, NavigableString, Tag

warnings.filterwarnings("ignore")


def get_data(URL):
    response = requests.get(URL)
    soups = BeautifulSoup(response.text, "html.parser")
    ### 주어진 데이터를 수집하여 csv 파일에 append 하여 저장하기
    try:
        soups_json = json.loads(soups.text)
        pd.DataFrame(soups_json["resources"]).to_csv(
            "bigdata_map_data.csv",
            mode="a",
            index=False,
            header=(not os.path.exists("bigdata_map_data.csv")),
        )
    except:
        pass


if __name__ == "__main__":
    ### 통합 데이터지도 홈페이지에서 구분해놓은 data 섹터를 리스트로 정의
    data_sector_lst = [
        "문화체육",
        "교육과학",
        "교통통신",
        "경제금융",
        "건설에너지",
        "농수산식품",
        "제조소비",
        "건강의료",
        "재난안전",
        "환경자원",
        "행정법률",
    ]

    ### 통합 데이터지도 홈페이지에서 각 섹터 및 페이지 별로 데이터의 정보를 가져와서 bigdata_map_data.csv 파일에 저장
    # ## CASE 1. 데이터의 양이 많기 때문에 1번에 1개씩 처리하는게 아닌, multiprocessing을 이용하여 병렬로 다수의 jobs을 처리
    # manager = multiprocessing.Manager()
    # jobs = []
    # for sector in tqdm(data_sector_lst):
    #     for page in range(1, 1000):
    #         URL = f"""https://www.bigdata-map.kr/api/search?typeFilters=일반(파일데이터)&largeFilters={sector}
    #             &sortMethod=score&page={page}&type=&reSearch=&history=&perPage=&platformType=&clickSearchKey=
    #             """

    #         p = multiprocessing.Process(target=get_data, args=(URL,))
    #         jobs.append(p)
    #         p.start()

    #     for proc in jobs:
    #         proc.join()

    #     time.sleep(60*10)

    ## CASE 2. 컴퓨팅 파워로 인해 multiprocessing이 제대로 동작하지 않을 수도 있기 때문에, 일반적으로 수집하는 형태의 코드
    for sector in tqdm(data_sector_lst):
        for page in tqdm(range(1, 1000)):
            URL = f"""https://www.bigdata-map.kr/api/search?typeFilters=일반(파일데이터)&largeFilters={sector}
                &sortMethod=score&page={page}&type=&reSearch=&history=&perPage=&platformType=&clickSearchKey=
                """
            get_data(URL)

        time.sleep(60 * 10)
