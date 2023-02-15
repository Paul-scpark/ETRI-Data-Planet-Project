import torch

import gluonnlp as nlp
from tqdm import tqdm

from transformers import AutoModel, AutoTokenizer, RobertaTokenizer, AutoModelForSequenceClassification
from transformers import AutoModelForMaskedLM, RobertaForSequenceClassification

from transformers.optimization import get_cosine_schedule_with_warmup

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import re

import os

import gc

gc.collect()
torch.cuda.empty_cache()

gpu_id = 0

device = (
        torch.device("cpu")
        if gpu_id < 0
        else torch.device("cuda:%d" % gpu_id)
    )

# HUGGINGFACE_MODEL_PATH = "rurupang/roberta-base-finetuned-sts"
# HUGGINGFACE_MODEL_PATH = "klue/roberta-base"
HUGGINGFACE_MODEL_PATH = "klue/roberta-small"

# roberta_tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

tokenizer = AutoTokenizer.from_pretrained(HUGGINGFACE_MODEL_PATH)

# model = AutoModelForSequenceClassification.from_pretrained("rurupang/roberta-base-finetuned-sts")
# tokenizer = AutoTokenizer.from_pretrained("rurupang/roberta-base-finetuned-sts", use_fast=True)

train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

train_df = train_df.dropna(axis=0)
test_df = test_df.dropna(axis=0)

from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()
label_encoder.fit(train_df['label'])
num_labels = len(label_encoder.classes_)

train_df['encoded_label'] = np.asarray(label_encoder.transform(train_df['label']), dtype=np.int32)
print(train_df.head())


test_df['encoded_label'] = np.asarray(label_encoder.transform(test_df['label']), dtype=np.int32)
print(test_df.head())


train_texts = train_df["description"].to_list() # Features (not-tokenized yet)
train_labels = torch.nn.functional.one_hot(torch.tensor(train_df["encoded_label"].to_list())) # Labels

test_texts = test_df["description"].to_list() # Features (not-tokenized yet)
test_labels = torch.nn.functional.one_hot(torch.tensor(test_df["encoded_label"].to_list())) # Labels


print(test_labels.size())

train_encodings = tokenizer(train_texts, truncation=True, padding=True, return_tensors="pt")
test_encodings = tokenizer(test_texts, truncation=True, padding=True, return_tensors="pt")

print(train_encodings)
print(train_encodings.input_ids)

from torch.utils.data import DataLoader, TensorDataset

train_data = TensorDataset(train_encodings.input_ids, train_encodings.attention_mask, train_labels)
train_dataloader = DataLoader(train_data, batch_size=8)

test_data = TensorDataset(test_encodings.input_ids, test_encodings.attention_mask, test_labels)
test_dataloader = DataLoader(test_data, batch_size=8)

print(train_data[0])


# model = RobertaForSequenceClassification.from_pretrained(HUGGINGFACE_MODEL_PATH, return_dict=False)
model = RobertaForSequenceClassification.from_pretrained(HUGGINGFACE_MODEL_PATH, num_labels=14, problem_type="multi_label_classification", return_dict=False)


from transformers import AdamW, get_linear_schedule_with_warmup

optimizer = AdamW(model.parameters(),
                  lr = 2e-5, 
                  eps = 1e-8 
                )

# Number of training epochs
epochs = 4

# Total number of training steps is number of batches * number of epochs.
total_steps = len(train_dataloader) * epochs

# Create the learning rate scheduler
scheduler = get_linear_schedule_with_warmup(optimizer,
                                            num_warmup_steps = 0,
                                            num_training_steps = total_steps)
loss_fn = torch.nn.CrossEntropyLoss(reduction='sum')
model.cuda()

batch_size = 8

def calc_accuracy(X, Y):
    max_vals, max_indices = torch.max(X, 1)
    train_acc = (max_indices == Y).sum().data.cpu().numpy() / max_indices.size()[0]
    return train_acc

# Training
import time
# Store the average loss after each epoch 
loss_values = []
# number of total steps for each epoch
print('total steps per epoch: ',  len(train_dataloader) / batch_size)
# looping over epochs
for epoch_i in range(0, epochs):
    
    torch.cuda.empty_cache()
    gc.collect()
    
    print('training on epoch: ', epoch_i)
    # set start time 
    t0 = time.time()
    # reset total loss
    total_loss = 0
    train_acc = 0.0
    # model in training 
    model.train()
    # loop through batch 
    for step, batch in enumerate(train_dataloader):
        # Progress update every 50 step 
        if step % 50 == 0 and not step == 0:
            print('training on step: ', step)
            print('total time used is: {0:.2f} s'.format(time.time() - t0))
        # load data from dataloader 
        b_input_ids = batch[0].to(device)
        b_input_mask = batch[1].to(device)
        b_labels = batch[2].float().to(device)
        # clear any previously calculated gradients 
        model.zero_grad()
        # get outputs
        outputs = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)
#         print(outputs)
#         print(b_labels)
#         loss = loss_fn(outputs, b_labels)
#         loss.backward()
        # get loss
        loss = outputs[0]
        # total loss
        total_loss += loss.item()
        # clip the norm of the gradients to 1.0.
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        # update optimizer
        optimizer.step()
        # update learning rate 
        scheduler.step()
#         train_acc += calc_accuracy(outputs, b_label)
#     print("epoch {} train acc {}".format(e + 1, train_acc / (step + 1)))
    # Calculate the average loss over the training data.
    avg_train_loss = total_loss / len(train_dataloader)
    # Store the loss value for plotting the learning curve.
    loss_values.append(avg_train_loss)
    print("average training loss: {0:.2f}".format(avg_train_loss))
    
    