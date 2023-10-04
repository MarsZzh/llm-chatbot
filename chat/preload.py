#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Author  ：zzh
@Date    ：2023/10/3 10:26
'''

from transformers import AutoTokenizer, AutoModel

model_name = "/mnt/workspace/work/model/chatglm2-6b"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name, trust_remote_code=True).cuda()
# 多显卡支持，使用下面两行代替上面一行，将num_gpus改为你实际的显卡数量
# from utils import load_model_on_gpus
# model = load_model_on_gpus("THUDM/chatglm2-6b", num_gpus=2)
model = model.eval()