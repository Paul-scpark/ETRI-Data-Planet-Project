import torch
import torch as nn
import pandas as pd
import numpy as np

import torch
from torch import nn

from torch.utils.data import DataLoader
import gluonnlp as nlp
from tqdm import tqdm
from sklearn.model_selection import train_test_split

from DistillKoBERT.loader import BERTDataset, koBERTDataset
from DistillKoBERT.utils import data_preprocess, calc_accuracy
from DistillKoBERT.DistillKoBERT_model.model import DistillKoBERTClassifier
# from .tokenization_kobert import KoBertTokenizer
from kobert_tokenizer import KoBERTTokenizer

from transformers import BertModel, DistilBertModel, DistilBertForSequenceClassification, AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

tokenizer = KoBERTTokenizer.from_pretrained("skt/kobert-base-v1")
tok = tokenizer._tokenize
# bertmodel = DistilBertForSequenceClassification.from_pretrained('monologg/distilkobert')
bertmodel = DistilBertModel.from_pretrained('monologg/distilkobert')
vocab = nlp.vocab.BERTVocab.from_sentencepiece(
    tokenizer.vocab_file, padding_token="[PAD]"
)

bert_model = torch.load("./DistillKoBERT/DistillKoBERT_model/_bert_only_5epochs.pt").to("cpu")

total_df = pd.read_csv("../total_data.csv")
total_data = []
data = []
for i in range(len(total_df)):
    data = []
    data.append(total_df["description"][i])
    data.append(0)
    total_data.append(data)


len(total_data)



total_data = np.array(total_data)


tokenizer = KoBERTTokenizer.from_pretrained("skt/kobert-base-v1")
tok = tokenizer.tokenize
# bertmodel = DistilBertForSequenceClassification.from_pretrained('monologg/distilkobert')
bertmodel = DistilBertModel.from_pretrained('monologg/distilkobert')
vocab = nlp.vocab.BERTVocab.from_sentencepiece(
    tokenizer.vocab_file, padding_token="[PAD]"
)

# %%
test_dataset = koBERTDataset(
    total_data, 0, 1, tok, vocab, 256, True, False
)

test_dataloader = DataLoader(
    test_dataset, batch_size=1, num_workers=5
)

# %%
# output2 = torch.cat([x,y], dim=2) #[M, N, K+K]
bert_model = bert_model.to("cpu")
result = torch.Tensor().to("cpu")
for token_ids, valid_length, segment_ids, label in test_dataloader:
    token_ids = token_ids.long().to("cpu")
    valid_length = valid_length.long().to("cpu")
    out = bert_model(token_ids, valid_length)
    result = torch.cat([result, out], dim=0)
    

print(result.shape)



