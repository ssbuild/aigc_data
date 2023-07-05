# -*- coding: utf-8 -*-
# @Time:  22:31
# @Author: tk
# @File：make_dataset
import json
import os

from fastdatasets.arrow.writer import PythonWriter
from fastdatasets.arrow.dataset import load_dataset,arrow
from fastdatasets import gfile



with_stream = False
def test_write(in_files,outfile):
    all_data = []
    for file in in_files:
        with open(file,mode='r',encoding='utf-8') as f:
            if os.path.basename(file).find('未完成') != -1:
                continue

            jds = json.loads(f.read())
            all_data.append((os.path.basename(file),jds))

    schema = {'id': 'int32',
              'instruction': 'str',
              'input': 'str',
              'output': 'str',
              'file': 'str',
              }
    fs = PythonWriter(outfile,
                        schema=schema,
                        with_stream=with_stream,
                        options=None)

    N = 1000
    for file, jds in all_data:
        batch = {k: [] for k in schema}
        for i, jd in enumerate(jds):
            batch["id"].append(i)
            batch["file"].append(file)

            for k,v in jd.items():
                if k == 'history':
                    continue
                batch[k].append(v)
            if 'input' not in jd:
                batch['input'].append('')

            if len(batch["id"]) % N == 0:
                fs.write_batch(batch.keys(), batch.values())
                for k,v in batch.items():
                    v.clear()
        if len(batch["id"]):
            fs.write_batch(batch.keys(), batch.values())
            for k, v in batch.items():
                v.clear()
    fs.close()

def test_random(file):
    dataset = load_dataset.RandomDataset(file,with_share_memory=not with_stream)
    print(file,'total', len(dataset))
    for i in range(len(dataset)):
        print(dataset[i])
        break



if __name__ == '__main__':

    in_files = [
        (gfile.glob(r'D:\cxx_project\alpaca_chinese_dataset\原始英文数据\*.json'),
         r'D:\cxx_project\alpaca_chinese_dataset\english.arrow'),
        (gfile.glob(r'D:\cxx_project\alpaca_chinese_dataset\翻译后的中文数据\*.json'),
         r'D:\cxx_project\alpaca_chinese_dataset\chinese.arrow'),
        (gfile.glob(r'D:\cxx_project\alpaca_chinese_dataset\其他中文问题补充\*.json'),
         r'D:\cxx_project\alpaca_chinese_dataset\other_chinese.arrow'),
    ]
    for files,outfile in in_files:
        test_write(files,outfile)
        test_random(outfile)
