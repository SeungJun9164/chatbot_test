# KoBART
# https://github.com/SKT-AI/KoBART

# KoBART Chatbot
# https://github.com/haven-jeon/KoBART-chatbot

# argparse
# https://greeksharifa.github.io/references/2019/02/12/argparse-usage/

# __getitem__ , __len__
# http://hyeonjae-blog.logdown.com/posts/776615-python-getitem-len

# logging
# https://greeksharifa.github.io/%ED%8C%8C%EC%9D%B4%EC%8D%AC/2019/12/13/logging/
# 소프트웨어가 작동 중일 때 발생하는 여러 ‘사건’을 추적하고, 개발자는 이를 통해 어떤 ‘사건’이 발생하였고 따라서 앞으로 어떤 해결책을 강구해야 할지 판단 / 이 중요도를 level


# pytorch-lightning
# https://baeseongsu.github.io/posts/pytorch-lightning-introduction/

import argparse
import logging
import os


import numpy as np
import pandas as pd
import pytorch_lightning as pl # pythorch_lightning 코드의 추상화 - 코드 스타일
import torch
from pytorch_lightning import loggers as pl_loggers # tensorborad와 같이 시각화 패키지
from torch.utils.data import DataLoader, Dataset
from transformers import (BartForConditionalGeneration, PreTrainedTokenizerFast)
from transformers.optimization import AdamW, get_cosine_schedule_with_warmup

parser = argparse.ArgumentParser(description = 'KOBART Chit-Chat')

# python kobart_test.py --subtask CoLA
parser.add_argument('--subtask', type=str, default='NSMC', help='NSMC, CoLA, QPair')

# python kobart_test.py --checkpoint_path ww
parser.add_argument('--checkpoint_path', type=str, help='checkpoint path')

# action='store_true, store_false' : 인자를 적으면(값은 주지 않는다) 해당 인자에 True나 False가 저장
# .py --chat -> True / .py -> False
parser.add_argument('--chat', action='store_true', default=False, help='response generation on given user input')

logger = logging.getLogger() # logger생성
logger.setLevel(logging.INFO) # 로그의 출력 기준 설정


class ArgsBase():
    @staticmethod
    def add_model_specific_args(parent_parser):
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)
        
        parser.add_argument('--train_file', type=str, default='Chatbot_data/train.csv',
                            help='train file')

        parser.add_argument('--test_file', type=str, default='Chatbot_data/train.csv',
                            help='test file')
        
        # tokenizer_path : emji tokenizer경로 설정
        parser.add_argument('--tokenizer_path', type=str, default='tokenizer', 
                            help='tokenizer')
        
        parser.add_argument('--batch_size', type=int, default=14,
                            help='')
        
        parser.add_argument('--max_seq_len', type=int, default=36,
                            help='max seq len')
        
        return parser

# csv파일에서 문장(단어) -> 토큰화 -> 인코딩화 시키는 함수
class ChatDataset():
    def __init__(self, filepath, tok_vocab, max_seq_len=128) -> None: # None : return 형
        self.filepath = filepath
        self.data = pd.read_csv(self.filepath)
        self.bos_token = '<s>'
        self.eos_token = '</s>'
        self.max_seq_len = max_seq_len
        self.tokenizer = PreTrainedTokenizerFast(tokenizer_file=tok_vocab,
                                                 bos_token=self.bos_token, eos_token=self.eos_token, unk_token='<unk>',
                                                 pad_token='<pad>', mask_token='<mask>')

    def __len__(self):
        return len(self.data)

    def make_input_id_mask(self, tokens, index):
        # input_id : [0, 19471, 15674, 14362, 14877, 21853, 14105, 15339, 245, 1]
        input_id = self.tokenizer.convert_tokens_to_ids(tokens)
        attention_mask = [1] * len(input_id)

        if len(input_id) < self.max_seq_len:
            while len(input_id) < self.max_seq_len:
                input_id += [self.tokenizer.pad_token_id]  # 최대 길이보다 짧을 시 pad_token으로 처리
                attention_mask += [0]
        else:
            # logging.warning(f'exceed max_seq_len for given article : {index}')
            input_id = input_id[:self.max_seq_len - 1] + [
                self.tokenizer.eos_token_id]
            attention_mask = attention_mask[:self.max_seq_len]

        return input_id, attention_mask

    def __getitem__(self, index):
        # recod : 좋아하는 남자 때문에 너무 기분이 안 좋아.,무슨 일이 있었나봐요.,2
        record = self.data.iloc[index]

        # q : 좋아하는 남자 때문에 너무 기분이 안 좋아. / a : 무슨 일이 있었나봐요.
        q, a = record['Q'], record['A']

        # q_tokens : ['<s>', '▁좋아하는', '▁남자', '▁때문에', '▁너무', '▁기분이', '▁안', '▁좋아', '.', '</s>']
        # a_tokens : ['<s>', '▁무슨', '▁일이', '▁있었', '나', '봐', '요.', '</s>']
        q_tokens = [self.bos_token] + self.tokenizer.tokenize(q) + [self.eos_token]
        a_tokens = [self.bos_token] + self.tokenizer.tokenize(a) + [self.eos_token]

        # encoder_input_id : (0, ..., 1, 3, 3, ...) (0 : bos_token = <s> , 1 : eos_token = </s>, 3 : pad_token)
        encoder_input_id, encoder_attention_mask = self.make_input_id_mask(q_tokens, index)
        decoder_input_id, decoder_attention_mask = self.make_input_id_mask(a_tokens, index)

        # labels : 마스킹 된 언어 모델링 손실을 계산하기위한 레이블
        # [16046, 15029, 14418,  9495, 10901, 14543, 1, -100, -100, ...]
        labels = self.tokenizer.convert_tokens_to_ids(a_tokens[1:(self.max_seq_len + 1)])

        if len(labels) < self.max_seq_len:
            while len(labels) < self.max_seq_len:
                # for cross entropy loss masking
                labels += [-100]

        return {'input_ids': np.array(encoder_input_id, dtype=np.int_),
                'attention_mask': np.array(encoder_attention_mask, dtype=np.float),
                'decoder_input_ids': np.array(decoder_input_id, dtype=np.int_),
                'decoder_attention_mask': np.array(decoder_attention_mask, dtype=np.float),
                'labels': np.array(labels, dtype=np.int_)}

# train, validation, test 데이터 설정하는 함수
class ChatDataModule(pl.LightningDataModule):
    def __init__(self, train_file, test_file, tok_vocab, max_seq_len=128, batch_size=32, num_workers=5):
        
        super().__init__()
        
        self.batch_size = batch_size
        self.max_seq_len = max_seq_len
        self.train_file_path = train_file
        self.test_file_path = test_file
        self.tok_vocab = tok_vocab
        self.num_workers = num_workers

        
    @staticmethod
    def add_model_specific_args(parent_parser):
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)
        
        parser.add_argument('--num_workers', type=int, default=5,
                            help='num of worker for dataloader')
        
        return parser

    # OPTIONAL, called for every GPU/machine (assigning state is OK)
    def setup(self, stage):
        # split dataset
        self.train = ChatDataset(self.train_file_path,
                                 self.tok_vocab,
                                 self.max_seq_len)
        
        self.test = ChatDataset(self.test_file_path,
                                self.tok_vocab,
                                self.max_seq_len)

    def train_dataloader(self):
        train = DataLoader(self.train, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=True)
        
        return train

    def val_dataloader(self):
        val = DataLoader(self.test, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=False)
        
        return val

    def test_dataloader(self):
        test = DataLoader(self.test, batch_size=self.batch_size, num_workers=self.num_workers, shuffle=False)
        
        return test


class Base(pl.LightningModule):
    def __init__(self, hparams, **kwargs) -> None:
        super(Base, self).__init__()
        self.hparams = hparams

    @staticmethod
    def add_model_specific_args(parent_parser):
        # add model specific args
        parser = argparse.ArgumentParser(parents=[parent_parser], add_help=False)

        parser.add_argument('--batch-size', type=int, default=14,
                            help='batch size for training (default: 96)')

        parser.add_argument('--lr', type=float, default=5e-5,
                            help='The initial learning rate')

        parser.add_argument('--warmup_ratio', type=float, default=0.1,
                            help='warmup ratio')

        parser.add_argument('--model_path', type=str, default=None,
                            help='kobart model path')
        return parser

    # huggingface의 transformers 가중치 설정하는 법
    # https://github.com/huggingface/transformers/issues/1218
    # https://www.programcreek.com/python/example/92667/torch.optim.Adam
    def configure_optimizers(self):
        # Prepare optimizer
        # param_optimizer : tuple형식
        # # named_parameters() : model이 어떻게 생겼는지 확인 model의 모든 파라미터 출력
        param_optimizer = list(self.model.named_parameters())
        no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {'params': [p for n, p in param_optimizer if not any(
                nd in n for nd in no_decay)], 'weight_decay': 0.01},
            {'params': [p for n, p in param_optimizer if any(
                nd in n for nd in no_decay)], 'weight_decay': 0.0}
        ]
        optimizer = AdamW(optimizer_grouped_parameters,
                          lr=self.hparams.lr, correct_bias=False)
        # warm up lr
        num_workers = (self.hparams.gpus if self.hparams.gpus is not None else 1) * (self.hparams.num_nodes if self.hparams.num_nodes is not None else 1)
        data_len = len(self.train_dataloader().dataset)
        logging.info(f'number of workers {num_workers}, data length {data_len}')
        num_train_steps = int(data_len / (self.hparams.batch_size * num_workers) * self.hparams.max_epochs)
        logging.info(f'num_train_steps : {num_train_steps}')
        num_warmup_steps = int(num_train_steps * self.hparams.warmup_ratio)
        logging.info(f'num_warmup_steps : {num_warmup_steps}')
        scheduler = get_cosine_schedule_with_warmup(
            optimizer,
            num_warmup_steps=num_warmup_steps, num_training_steps=num_train_steps)
        lr_scheduler = {'scheduler': scheduler, 
                        'monitor': 'loss', 'interval': 'step',
                        'frequency': 1}
        return [optimizer], [lr_scheduler]


class KoBARTConditionalGeneration(Base):
    def __init__(self, hparams, **kwargs):
        super(KoBARTConditionalGeneration, self).__init__(hparams, **kwargs)
        self.model = BartForConditionalGeneration.from_pretrained(self.hparams.model_path)
        self.model.train()
        self.bos_token = '<s>'
        self.eos_token = '</s>'
        self.tokenizer = PreTrainedTokenizerFast(tokenizer_file=os.path.join(self.hparams.tokenizer_path, 'model.json'),
                                                bos_token=self.bos_token, eos_token=self.eos_token, unk_token='<unk>', pad_token='<pad>', mask_token='<mask>')
        
    def forward(self, inputs):
        return self.model(input_ids=inputs['input_ids'],
                          attention_mask=inputs['attention_mask'],
                          decoder_input_ids=inputs['decoder_input_ids'],
                          decoder_attention_mask=inputs['decoder_attention_mask'],
                          labels=inputs['labels'], return_dict=True)
    
    def training_step(self, batch, batch_idx):
        outs = self(batch)
        loss = outs.loss
        self.log('train_loss', loss, prog_bar=True)
        
        return loss
    
    def validation_step(self, batch, batch_idx):
        outs = self(batch)
        loss = outs['loss']
        
        return (loss)
    
    def validation_epoch_end(self, outputs):
        losses = []
        for loss in outputs:
            losses.append(loss)
        self.log('val_loss', torch.stack(losses).mean(), prog_bar=True)
        
    def chat(self, text):
        input_ids = [self.tokenizer.bos_token_id] + self.tokenizer.encode(text) + [self.tokenizer.eos_token_id]
        res_ids = self.model.generate(torch.tensor([input_ids]), 
                                      max_length=self.hparams.max_seq_len, 
                                      num_beams=5, 
                                      eos_token_id=self.tokenize.eos_token_id, 
                                      bad_words_ids=[[self.tokenizer.unk_token_id]])
        
        a = self.tokenizer.batch_decode(res_ids.tolist())[0]
        return a.replace('<s>', '').replace('</s>', '')


if __name__ == '__main__':
    parser = Base.add_model_specific_args(parser)
    parser = ArgsBase.add_model_specific_args(parser)
    parser = ChatDataModule.add_model_specific_args(parser)
    parser = pl.Trainer.add_argparse_args(parser)
    args = parser.parse_args()
    logging.info(args)
    
    model = KoBARTConditionalGeneration(args)
    
    dm = ChatDataModule(args.train_file, args.test_file, os.path.join(args.tokenizer_path, 'model.json'),
                                                                     max_seq_len=args.max_seq_len,
                                                                     num_workers=args.num_workers)
    # checkpoint 저장
    checkpoint_callback = pl.callbacks.ModelCheckpoint(monitor='val_loss',
                                                       dirpath=args.default_root_dir, 
                                                       filename='model_chp/{epoch_02d}-{val_loss:.3f}', 
                                                       verbose=True, 
                                                       save_last=True, mode='min', 
                                                       save_top_k = -1, 
                                                       prefix='kobert_chitchat')
    
    tb_logger = pl_loggers.TensorBoardLogger(os.path.join(args.default_root_dir, 'tb_logs'))
    lr_logger = pl.callbacks.LearningRateMonitor()
    trainer = pl.Trainer.from_argparse_args(args, logger=tb_logger, callbacks=[checkpoint_callback, lr_logger])
    
    trainer.fit(model, dm)
    
    if args.chat:
        model.model.eval()
        while 1:
            q = input('user > ').strip()
            if q == 'quit':
                break
            print('Simsimi > {}'.format(model.chat(q)))

from kobart import get_pytorch_kobart_model, get_kobart_tokenizer
get_kobart_tokenizer(".")
get_pytorch_kobart_model(cachedir=".")


# 실행방법
# kobart_chit_chat.py  --gradient_clip_val 1.0 --max_epochs 3 --default_root_dir logs --model_path kobart_from_pretrained  --tokenizer_path emji_tokenizer --chat --gpus 1





