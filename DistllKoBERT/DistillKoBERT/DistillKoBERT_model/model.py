import torch
import torch.nn as nn


class DistillKoBERTClassifier(nn.Module):
    def __init__(
        self, bert, hidden_size=768, num_classes=14, dr_rate=None, params=None):
        super(DistillKoBERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        # self.classifier = nn.Linear(hidden_size, num_classes)
        # if dr_rate:
        #     self.dropout = nn.Dropout(p=dr_rate)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
            
        return attention_mask.float()

    def forward(self, token_ids, valid_length):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)

        out = self.bert(input_ids=token_ids,
            attention_mask=attention_mask.to(token_ids.device)
        )
        
        hidden_state = out[0]
        out = hidden_state[:, 0]

        # if self.dr_rate:
        #     out = self.dropout(out)
            
        # out = self.classifier(out)
        return out 
