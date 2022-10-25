import torch
from torch import nn
from torch.utils.data import DataLoader
import pandas as pd
import gluonnlp as nlp
import numpy as np
import csv

from transformers import BertModel
from kobert_tokenizer import KoBERTTokenizer
from koBERT.utils import new_softmax, data_preprocess
from koBERT.loader import koBERTDataset

from sklearn.metrics import accuracy_score, f1_score

import argparse


def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument('--model_name', required=True)
    p.add_argument('--gpu_id', type=int, default=0)
    p.add_argument('--batch_size', type=int, default=64)
    p.add_argument('--dropout_p', type=float, default=.5)
    p.add_argument('--learning_rate', type=float, default=5e-5)
    p.add_argument('--warmup_ratio', type=float, default=0.1)
    p.add_argument('--max_len', type=int, default=64)
    p.add_argument('--num_epochs', type=int, default=5)
    p.add_argument('--max_grad_norm', type=int, default=1)
    p.add_argument('--log_interval', type=int, default=200)

    config = p.parse_args()
    return config


def main(config):
    device = torch.device('cpu') if config.gpu_id < 0 else torch.device('cuda:%d' % config.gpu_id)

    tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
    tok = tokenizer.tokenize

    bertmodel = BertModel.from_pretrained('skt/kobert-base-v1', return_dict=False)
    vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')

    temp_df = pd.read_csv("./data/test.csv")
    correct_label = temp_df['cat1']
    test_data = data_preprocess("./data/test.csv")

    data_test = koBERTDataset(test_data, 0, 1, tok, vocab, config.max_len, True, False)
    test_dataloader = DataLoader(data_test, batch_size=config.batch_size, num_workers=5)

    PATH = 'koBERT/koBERT_model/'
    model = torch.load(PATH + '_' + config.model_name + '.pt')
    model.load_state_dict(torch.load(PATH + '_' + config.model_name + '_state_dict.pt')) 
    model.eval()
    result = []
    for _, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)
        valid_length= valid_length
        label = label.long().to(device)
        out = model(token_ids, valid_length, segment_ids)
        for i in out:
            logits=i
            logits = logits.detach().cpu().numpy()
            probability = []
            logits = np.round(new_softmax(logits), 3).tolist()
            for logit in logits:
                print(logit)
                probability.append(np.round(logit, 3))
            if np.argmax(logits) == 0:  emotion = "레포츠"
            elif np.argmax(logits) == 1: emotion = "쇼핑"
            elif np.argmax(logits) == 2: emotion = '숙박'
            elif np.argmax(logits) == 3: emotion = '음식'
            elif np.argmax(logits) == 4: emotion = '인문(문화/예술/역사)'
            elif np.argmax(logits) == 5: emotion = '자연'
            probability.append(emotion)

            result.append(emotion)

    with open('./result.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow(result)


    print(f"accuacy : {accuracy_score(correct_label, result)}")
    print(f"weighted_f1_score : {f1_score(y_true = correct_label, y_pred = result, average = 'weighted')}")



if __name__ == '__main__':
    config = define_argparser()
    main(config)


