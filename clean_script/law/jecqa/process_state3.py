# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/10/17 11:10
import os
import random
import pandas as pd
import glob

random.seed(42)

def make_evals(fs_list,output_dir,shuffle=False,limit_single=-1,limit_muti=-1):
    os.makedirs(os.path.join(output_dir, "single"),exist_ok=True)
    os.makedirs(os.path.join(output_dir, "muti"), exist_ok=True)
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

        if shuffle:
            random.shuffle(singles)
            random.shuffle(mutis)
        if limit_single > 0:
            singles = singles[:limit_single]

        if limit_muti > 0:
            mutis = mutis[:limit_muti]

        df_single = pd.DataFrame(singles)
        df_muti = pd.DataFrame(mutis)


        basename = os.path.basename(filename)
        df_single.to_csv(os.path.join(output_dir,"single",basename),index=False)
        df_muti.to_csv(os.path.join(output_dir, "muti", basename),index=False)


if __name__ == '__main__':
    # 将评估dev数据集 , 制作成 aigc_evals 评估格式
    fs_list = glob.glob(r'F:\nlpdata_2023\JEC-QA\clean\dev\*.csv')
    make_evals(fs_list,
               r'F:\nlpdata_2023\JEC-QA\clean\evals\dev')

    # 将评估train数据集 , 制作成 aigc_evals 评估格式
    fs_list = glob.glob(r'F:\nlpdata_2023\JEC-QA\clean\train\*.csv')
    make_evals(fs_list,
               r'F:\nlpdata_2023\JEC-QA\clean\evals\train',
               shuffle=True,limit_single=400,limit_muti=400)