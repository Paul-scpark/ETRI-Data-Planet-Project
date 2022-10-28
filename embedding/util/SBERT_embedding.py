import torch
import os
from tqdm import tqdm
tqdm.pandas()
import time

class create_sbert_embedding:
    def __init__(self, df, model):
        # total_data.csv
        self.df = df
        # pre-trained SBERT
        self.model = model

    def create_emb(self):
        start = time.time()
        print("description values embedding start..")
        target = self.df['description']
        # target_encode = target.progress_map(lambda x: self.model.encode(x))
        target_encode = self.model.encode(target)
        des_emb = torch.tensor(target_encode)
        torch.save(des_emb, 'C:/Users/Home/Documents/GitHub/AI-dev-course-prj/data/des_embedding.pt')
        end = time.time()
        print(f"create done.. Time elapsed : {end-start:.5f} sec")