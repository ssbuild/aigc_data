# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/6/8 10:43
import json
import os
from fastdatasets.record.writer import JsonWriter
from fastdatasets.record import load_dataset as Loader,gfile,RECORD,DataType,BytesWriter



def test_write(in_files,outfile, compression_type='GZIP'):
    all_data = []
    for file in in_files:
        with open(file, mode='r', encoding='utf-8') as f:
            if os.path.basename(file).find('未完成') != -1:
                continue

            jds = json.loads(f.read())
            all_data.append((os.path.basename(file), jds))


    options = RECORD.TFRecordOptions(compression_type=compression_type)
    writer = JsonWriter(outfile, options)
    N = 1000
    for file, jds in all_data:
        batch = []
        for i, jd in enumerate(jds):
            batch.append(jd)
            if len(batch) % N == 0:
                writer.write_batch(batch)
                batch.clear()
        if len(batch):
            writer.write_batch(batch)
            batch.clear()
    writer.close()




def test_random(file, limit=2, compression_type='GZIP'):
    options = RECORD.TFRecordOptions(compression_type=compression_type)
    dataset = Loader.RandomDataset(file, options=options)
    print(file, 'total', len(dataset))
    for i in range(len(dataset)):
        d = dataset[i]
        if i >= limit:
            break
        d = json.loads(d)
        print(d)
    dataset.close()


if __name__ == '__main__':

    if __name__ == '__main__':

        in_files = [
            (gfile.glob(r'../alpaca_chinese_dataset/原始英文数据/*.json'),
             r'../alpaca_chinese_dataset/english.record'),
            (gfile.glob(r'../alpaca_chinese_dataset/翻译后的中文数据/*.json'),
             r'../alpaca_chinese_dataset/chinese.record'),
            (gfile.glob(r'../alpaca_chinese_dataset/其他中文问题补充/*.json'),
             r'../alpaca_chinese_dataset/other_chinese.record'),
        ]
        for files, outfile in in_files:
            test_write(files, outfile)
            test_random(outfile)
