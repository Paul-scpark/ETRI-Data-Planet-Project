import os
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from random import randrange

# util 작성 코드
from util.create_SBERT_embedding import create_sbert_embedding


def print_data_info(df, random_idx):
    print("data title : " + df["title"][random_idx])
    print("data description : " + df["description"][random_idx])
    print("data url : " + df["url"][random_idx])
    print("data type : " + df["data_type"][random_idx])
    print("data source : " + df["source"][random_idx])
    print("data ori_label : " + df["ori_label"][random_idx])
    print("data ori_source : " + df["ori_source"][random_idx])
    print("data label : " + df["label"][random_idx])
    print("\n")


if __name__ == "__main__":
    # total_data.csv 불러오기
    print("total_data.csv load..")
    df = pd.read_csv("data/total_data.csv")

    # SBERT model 불러오기
    print("load SBERT model..")

    model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")

    # total_data의 description embedding 불러오기
    if not os.path.isfile("data/des_embedding.pt"):
        print("create description embedding..")
        create_pt = create_sbert_embedding(df=df, model=model)
        create_pt.create_emb()

    print("load descripton embedding..")
    des_emb = torch.load("data/des_embedding.pt")

    # 랜덤 인덱스 선택 및 데이터 정보 출력
    random_idx = randrange(len(df))
    print(f"랜덤 선택된 idx: {random_idx}")
    print("선택된 랜덤 인덱스의 데이터 정보:")
    print_data_info(df, random_idx)

    # calculate distance with SBERT
    distance = util.cos_sim(des_emb[random_idx], des_emb)
    sort_distance = distance[0].sort()

    for i in sort_distance.indices[-6:-1].tolist():
        print_data_info(df, i)
