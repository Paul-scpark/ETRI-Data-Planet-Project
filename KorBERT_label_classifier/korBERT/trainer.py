import torch
from torch import nn
from torch.utils.data import DataLoader
import gluonnlp as nlp
from tqdm import tqdm


from korBERT.loader import korBERTDataset
from korBERT.utils import data_preprocess, calc_accuracy, EarlyStopping
from korBERT.korBERT_model.model import korBERTClassifier
from pytorch_pretrained_bert.tokenization import BertTokenizer
from pytorch_pretrained_bert.modeling import BertModel, BertConfig


from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup



def train(config):
    device = torch.device('cpu') if config.gpu_id < 0 else torch.device('cuda:%d' % config.gpu_id)


    tokenizer = BertTokenizer("./vocab.korean.rawtext.list", do_lower_case=False)
    tok = tokenizer.tokenize
    vocab = nlp.vocab.BERTVocab(tokenizer.vocab, padding_token='[PAD]')

    bert_config = BertConfig.from_json_file("./bert_config.json")
    bert_model = BertModel(config=bert_config)
    bert_model.init_bert_weights(torch.load("./pytorch_model.bin"))


    train_data, _ = data_preprocess("./train.csv")
    valid_data, _ = data_preprocess("./valid.csv")
   

    train_dataset = korBERTDataset(train_data, 0, 1, tok, vocab, config.max_len, True, False)
    valid_dataset = korBERTDataset(valid_data, 0, 1, tok, vocab, config.max_len, True, False)

    train_dataloader = DataLoader(train_dataset, batch_size=config.batch_size, num_workers=5)
    valid_dataloader = DataLoader(valid_dataset, batch_size=config.batch_size, num_workers=5)

    model = korBERTClassifier(bert_model,  dr_rate=config.dropout_p).to(device)

    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]


    optimizer = AdamW(optimizer_grouped_parameters, lr=config.learning_rate)
    loss_fn = nn.CrossEntropyLoss()
    t_total = len(train_dataloader) * config.num_epochs
    warmup_step = int(t_total * config.warmup_ratio)
    scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=warmup_step, num_training_steps=t_total)
    early_stopping = EarlyStopping(patience = 3, verbose = True)

    for e in range(config.num_epochs):
        train_acc = 0.0
        test_acc = 0.0
        test_loss = 0.0
        model.train()
        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm(train_dataloader)):
            optimizer.zero_grad()
            token_ids = token_ids.long().to(device)
            segment_ids = segment_ids.long().to(device)
            valid_length= valid_length
            label = label.long().to(device)
            out = model(token_ids, valid_length, segment_ids)
            loss = loss_fn(out, label)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.max_grad_norm)
            optimizer.step()
            scheduler.step()  # Update learning rate schedule
            train_acc += calc_accuracy(out, label)
            # if batch_id % config.log_interval == 0:
            #     print("epoch {} batch id {} loss {} train acc {}".format(e+1, batch_id+1, loss.data.cpu().numpy(), train_acc / (batch_id+1)))
        print("epoch {} train acc {}".format(e+1, train_acc / (batch_id+1)))
        model.eval()
        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm(valid_dataloader)):
            token_ids = token_ids.long().to(device)
            segment_ids = segment_ids.long().to(device)
            valid_length= valid_length
            label = label.long().to(device)
            out = model(token_ids, valid_length, segment_ids)
            temp_test_loss = loss_fn(out, label)
            test_loss += temp_test_loss.item()    
            test_acc += calc_accuracy(out, label)
        print("epoch {} valid acc {}".format(e+1, test_acc / (batch_id+1)))
        early_stopping(test_loss, model)
        if early_stopping.early_stop:
            break


    PATH = './korBERT/korBERT_model/'
    torch.save(model, PATH + config.model_name + '.pt')
    torch.save(model.state_dict(), PATH + config.model_name + '_state_dict.pt')  