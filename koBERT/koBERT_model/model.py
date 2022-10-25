import torch
import torch.nn as nn

class koBERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size = 768,
                 num_classes=14,
                 dr_rate=None,
                 params=None):
        super(koBERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate
                 
        self.classifier = nn.Linear(hidden_size , num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)
    
    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)
        
        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)


class koBERTClassifier_cat3(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size = 768,
                 num_classes=128,
                 dr_rate=None,
                 params=None):
        super(koBERTClassifier_cat3, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate
        self.num_classes = num_classes
        

        # activation function 추가
        # 아........
        # 여기에 추가한다고 해서 성능이 좋아지지 않음!
        # 서로 다른 model에서 추출된 feature에 대해서 layer를 쌓는것이 목적
        # optuna에 layer 최적화 기능이 있다 -> 실험을 해보는것도 의미가 있음
    
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size , 256),
            nn.Linear(256 , 128),
            nn.Linear(128 , self.num_classes)
        )
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)
    
    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)
        
        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)