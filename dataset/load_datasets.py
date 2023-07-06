# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/7/6 11:05

from datasets import load_dataset

dataset = load_dataset("ssbuild/alpaca_chinese_dataset")

print(dataset)