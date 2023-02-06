import torch
import time
import pandas as pd
from sentence_transformers import SentenceTransformer

def create_embedding():
    df = pd.read_csv("data/total_data.csv")
    model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')
    start = time.time()
    des = df["description"]
    title = df["title"]

    # description embedding
    print('create description embedding...')
    des_encode = model.encode(des)
    des_emb = torch.tensor(des_encode)
    torch.save(des_emb, "data/des_emb_SBERT.pt")

    # title embedding
    print('create title embedding...')
    title_encode = model.encode(title)
    title_emb = torch.tensor(title_encode)
    torch.save(title_emb, "data/title_emb_SBERT.pt")

    end = time.time()
    print(f"done.. Time elapsed : {end - start:.5f} sec")

create_embedding()
