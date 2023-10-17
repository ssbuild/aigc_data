# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/10/16 13:59
import glob
import json
import os.path
import random
import pandas as pd
random.seed(123456)

# 数据下载 https://jecqa.thunlp.org/

def extract_data_from_jec(jec_files,out_dir):
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "train"),exist_ok=True)
    os.makedirs(os.path.join(out_dir, "dev"),exist_ok=True)

    lines = []
    for filename in jec_files:
        with open(filename, mode='r', encoding='utf-8') as f:
            lines += f.readlines()
    labels = {}
    for line in lines:
        jd = json.loads(line)
        if not jd:
            continue
        if "subject" not in jd:
            jd["subject"] = "unlabel"

        jd["answer"] = eval(jd["answer"]) if isinstance(jd["answer"],str) else jd["answer"]
        if jd["subject"] not in labels:
            labels[jd["subject"]] = []
        labels[jd["subject"]].append(jd)


    def save_data(v,filename):
        new_jds = []
        for i, jd in enumerate(v):
            # id,question,A,B,C,D,answer
            new_jd = {}
            option_list = jd["option_list"]
            assert len(option_list) == 4
            new_jd["id"] = i
            new_jd["question"] = jd["statement"]
            new_jd["A"] = option_list["A"]
            new_jd["B"] = option_list["B"]
            new_jd["C"] = option_list["C"]
            new_jd["D"] = option_list["D"]
            new_jd["answer"] = jd["answer"]
            new_jds.append(new_jd)
        pd.DataFrame(new_jds).to_csv(filename, index=False)

    for k,v in labels.items():
        random.shuffle(v)
        limit_n = int(len(v) * 0.25)
        limit_n = min(limit_n,180)
        train_v = v[limit_n:]
        val_v = v[:limit_n]


        save_data(train_v, os.path.join(out_dir,"train",k + '.csv'))
        save_data(val_v, os.path.join(out_dir,"dev",k + '.csv'))



if __name__ == '__main__':

    jec_files = glob.glob(r"F:\nlpdata_2023\JEC-QA\*_train.json")
    out_dir = r"F:\nlpdata_2023\JEC-QA\clean"
    extract_data_from_jec(jec_files,out_dir)

