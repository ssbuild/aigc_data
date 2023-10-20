# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/10/17 11:10
import os.path

import pandas as pd
import glob


fs_list = glob.glob(r'F:\nlpdata_2023\JEC-QA\clean\dev\*.csv')
os.makedirs(r"F:\nlpdata_2023\JEC-QA\clean\dev_single",exist_ok=True)
os.makedirs(r"F:\nlpdata_2023\JEC-QA\clean\dev_muti",exist_ok=True)


# 将评估dev数据集 , 制作成 aigc_evals 评估格式

for filename in fs_list:
    df = pd.read_csv(filename)

    singles,mutis = [],[]
    n1,n2 = 0,0
    idx_ = 0
    for idx, question, A, B, C, D, answer in zip(df["id"], df["question"], df["A"], df["B"], df["C"], df["D"],
                                                 df["answer"]):
        answer = eval(answer)
        if len(answer) == 1:
            n1 += 1
            n = n1
            result = singles
        else:
            n2 += 1
            n = n2
            result = mutis

        idx_ += 1

        result.append({
            "id": n,
            "question": question,
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "answer": answer,
        })


    df_single = pd.DataFrame(singles)
    df_muti = pd.DataFrame(mutis)

    dirname = os.path.join(os.path.dirname(filename),'..')
    basename = os.path.basename(filename)
    df_single.to_csv(os.path.join(dirname,"dev_single",basename),index=False)
    df_muti.to_csv(os.path.join(dirname, "dev_muti", basename),index=False)