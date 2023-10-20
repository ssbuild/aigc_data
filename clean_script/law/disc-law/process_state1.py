# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/10/20 9:51
import json
import os
import pandas as pd
from collections import OrderedDict
import glob

# 将数据制作成 aigc evals 评估格式

# 数据下载地址 https://github.com/FudanDISC/DISC-LawLLM/tree/main/eval/data

fs_list = glob.glob(r'F:\nlpdata_2023\DISC-Law\data\objective_eval\test\*.csv')
os.makedirs(os.path.join(r'F:\nlpdata_2023\DISC-Law', "dev_single"), exist_ok=True)
os.makedirs(os.path.join(r'F:\nlpdata_2023\DISC-Law', "dev_muti"), exist_ok=True)

D_single,D_muti = [] , []
for filename in fs_list:
    df = pd.read_csv(filename)
    for i in range(len(df)):
        d = OrderedDict()
        for k in df.keys():
            d[k] = df[k].iloc[i]
        multichoice = d.pop("multichoice")
        # w_jd["id"] = i
        # new_jd["question"] = jd["statement"]
        # new_jd["A"] = option_list["A"]
        # new_jd["B"] = option_list["B"]
        # new_jd["C"] = option_list["C"]
        # new_jd["D"] = option_list["D"]
        # new_jd["answer"] = jd["answer"]

        d_ = {}
        d_["id"] = i + 1
        d_["question"] = d["input"]
        d_["A"] = d["A"]
        d_["B"] = d["B"]
        d_["C"] = d["C"]
        d_["D"] = d["D"]
        d_["answer"] = d["output"]

        if multichoice:
            D = D_muti
            d_["answer"] = list(d_["answer"])
        else:
            D = D_single
        D.append(d_)

    df_single = pd.DataFrame(D_single)
    df_muti = pd.DataFrame(D_muti)

    file = os.path.basename(filename)
    df_single.to_csv(os.path.join(r'F:\nlpdata_2023\DISC-Law',"dev_single",file), index=False)
    df_muti.to_csv(os.path.join(r'F:\nlpdata_2023\DISC-Law',"dev_muti",file), index=False)

