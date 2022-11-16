import torch
from torch import nn
from torch.utils.data import DataLoader
import gluonnlp as nlp
from tqdm import tqdm
import numpy as np

from korBERT.loader import korBERTDataset
from korBERT.utils import calc_accuracy, EarlyStopping, new_softmax
from korBERT.korBERT_model.model import korBERTClassifier
from pytorch_pretrained_bert.tokenization import BertTokenizer
from pytorch_pretrained_bert.modeling import BertModel, BertConfig


from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup


def predict(config, text):
    device = (
        torch.device("cpu")
        if config.gpu_id < 0
        else torch.device("cuda:%d" % config.gpu_id)
    )
    encoder = [
        "경제금융",
        "교육과학",
        "교통물류",
        "기타",
        "문화관광",
        "보건의료",
        "사회복지",
        "식품건강",
        "재난안전",
        "제조소비",
        "주택토지",
        "통일외교안보",
        "행정법률",
        "환경기상",
    ]

    tokenizer = BertTokenizer("./vocab.korean.rawtext.list", do_lower_case=False)
    tok = tokenizer.tokenize
    vocab = nlp.vocab.BERTVocab(tokenizer.vocab, padding_token="[PAD]")

    model = torch.load("./korBERT/korBERT_model/korBERT_model2.pt").to(device)

    predict_data = [[text, 0]]
    predict_dataset = korBERTDataset(
        predict_data, 0, 1, tok, vocab, config.max_len, True, False
    )
    predict_dataloader = DataLoader(predict_dataset, batch_size=1, num_workers=5)

    results = []
    for (token_ids, valid_length, segment_ids, label) in predict_dataloader:
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)
        valid_length = valid_length
        label = label.long().to(device)
        out = model(token_ids, valid_length, segment_ids)
        for i in out:
            logits = i
            logits = logits.detach().cpu().numpy()
            probability = []
            logits = np.round(new_softmax(logits), 3).tolist()
            temp = encoder[np.argmax(logits)]
            results.append(temp)

    return results[0]
