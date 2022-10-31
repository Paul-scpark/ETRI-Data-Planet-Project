import torch
from torch import nn
from torch.utils.data import DataLoader
import gluonnlp as nlp
from tqdm import tqdm
import numpy as np
import pandas as pd
import os.path
import collections
from korBERT.loader import korBERTDataset
from korBERT.utils import data_preprocess, cos_sim
from pytorch_pretrained_bert.tokenization import BertTokenizer



def get_similarity(text):
    print(torch.cuda.is_available())
    device = torch.device('cpu') if torch.cuda.is_available() == False else torch.device('cuda:0')
    file = "data_feature.npy"
    if os.path.isfile(file) == False:
        print("-"*5,"No data File","-"*5)
        print("-"*5,"Create data File","-"*5)

        

        tokenizer = BertTokenizer("./vocab.korean.rawtext.list", do_lower_case=False)
        tok = tokenizer.tokenize
        vocab = nlp.vocab.BERTVocab(tokenizer.vocab, padding_token='[PAD]')

        model = torch.load("./korBERT/korBERT_model/similarity_model.pt").to(device)

        full_data, _ = data_preprocess("./total_data.csv")
        full_dataset = korBERTDataset(full_data, 0, 1, tok, vocab, 64, True, False)
        full_dataloader = DataLoader(full_dataset, batch_size=1024, num_workers=5)

        results = []
        model.eval()
        with torch.no_grad():
            for (token_ids, valid_length, segment_ids, label) in tqdm(full_dataloader):
                token_ids = token_ids.long().to(device)
                segment_ids = segment_ids.long().to(device)
                valid_length= valid_length
                label = label.long().to(device)
                _, feature = model(token_ids, valid_length, segment_ids)
                results.append(feature.detach().cpu().numpy())

            # results = torch.tensor(results)
            results = np.array(results)
            print(results)
            np.save("./data_feature.npy", results)

    else:
        print("file is available")
        feature_array = np.load("./data_feature.npy", allow_pickle=True)

        display_data = pd.read_csv("./total_data.csv")
        display_data.dropna(axis=0, inplace=True)


        tokenizer = BertTokenizer("./vocab.korean.rawtext.list", do_lower_case=False)
        tok = tokenizer.tokenize
        vocab = nlp.vocab.BERTVocab(tokenizer.vocab, padding_token='[PAD]')

        model = torch.load("./korBERT/korBERT_model/similarity_model.pt").to(device)

        predict_data = [[text, 0]]
        predict_dataset = korBERTDataset(predict_data, 0, 1, tok, vocab, 64, True, False)
        predict_dataloader = DataLoader(predict_dataset, batch_size=1, num_workers=5)

        model.eval()
        with torch.no_grad():
            for (token_ids, valid_length, segment_ids, label) in predict_dataloader:
                token_ids = token_ids.long().to(device)
                segment_ids = segment_ids.long().to(device)
                valid_length= valid_length
                label = label.long().to(device)
                _, text_feature = model(token_ids, valid_length, segment_ids)
                text_feature= text_feature.detach().cpu().numpy()
            

        reshaped_feature = []
        for epoch in feature_array:
            for iter in epoch:
                reshaped_feature.append(iter)

        reshaped_feature = np.array(reshaped_feature)

        index_deq = collections.deque([])
        high_score = 0.0
        for index, feat in enumerate(reshaped_feature):
            temp_score = cos_sim(feat, text_feature.squeeze())
            if high_score < temp_score:
                high_score = temp_score
                high_index = index

        print(high_index, type(high_index))
        print(display_data.iloc[high_index])


        
        # index_deq.append(index)
        
        # for index, feat in enumerate(reshaped_feature):
        #     temp_score = cos_sim(feat, text_feature.squeeze())
        #     if high_score < temp_score:
        #         index_deq.append(index)
        #     if len(index_deq) > 5:
        #         index_deq.popleft()



        # print(list(reversed(index_deq)))
        # for index in list(reversed(index_deq)):
        #     print(display_data.iloc[index,:])