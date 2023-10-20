# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/10/17 10:37
import glob
import json

import pandas as pd



# w_jd["id"] = i
# new_jd["question"] = jd["statement"]
# new_jd["A"] = option_list["A"]
# new_jd["B"] = option_list["B"]
# new_jd["C"] = option_list["C"]
# new_jd["D"] = option_list["D"]
# new_jd["answer"] = jd["answer"]

# 将切分的训练评估数据集，制作成可训练格式

def dump_write(fs_list,outfile):
    with open(outfile,mode='w',encoding='utf-8') as f:
        idx_ = 0
        for filename in fs_list:
            df = pd.read_csv(filename)
            for idx,question,A,B,C,D,answer in zip(df["id"],df["question"],df["A"],df["B"],df["C"],df["D"],df["answer"]):
                answer = eval(answer)

                prefix = "以下是一道单项选择题" if len(answer) == 1 else "以下是一道多项选择题"
                prefix += '\n\n'
                input = prefix + question + '\n' + f"A.{A}\n" + f"B.{B}\n"+ f"C.{C}\n"+ f"D.{D}\n"
                output = "正确答案是: " + ','.join(answer)

                idx_ += 1
                f.write(json.dumps({
                    "id": idx_,
                    "paragraph":[
                        {
                            "q": input,
                            "a": output
                        }
                    ]

                },ensure_ascii=False) + '\n')



fslist = glob.glob(r"F:\nlpdata_2023\JEC-QA\clean\dev\*.csv")
dump_write(fslist,r'F:\nlpdata_2023\JEC-QA\clean\dev_exam.json')

fslist = glob.glob(r"F:\nlpdata_2023\JEC-QA\clean\train\*.csv")
dump_write(fslist,r'F:\nlpdata_2023\JEC-QA\clean\train_exam.json')