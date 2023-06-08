# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/6/8 10:43
import json
import os
import random
import data_serialize
from tqdm import tqdm
import numpy as np
from datetime import datetime
from fastdatasets.record import load_dataset as Loader,gfile,RECORD,DataType,BytesWriter
import fastcrypto


# ,key,iv  length must 16
# key iv 元素取值范围 0-255  一共有 255 的 16次方 * 255 的 16次方 种秘钥

key = bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
iv = bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
def encode_data(data: bytes):
    ret = fastcrypto.aes_encode(data, key, iv)
    assert ret[0] == 0
    crypt_data = ret[1]
    return crypt_data

def decode_data(data: bytes):
    ret = fastcrypto.aes_decode(data, key, iv)
    assert ret[0] == 0
    return ret[1]


def write_record(src_file,dst_file,compression_type='GZIP'):
    with open(src_file,mode='r',encoding='utf-8',newline='\n') as f:
        lines = f.readlines()
        options = RECORD.TFRecordOptions(compression_type=compression_type)
        writer = BytesWriter(dst_file, options)
        for line in tqdm(lines,desc='write record'):
            if not line:
                continue
            data = bytes(line,encoding='utf-8')
            data = encode_data(data)
            writer.write(data)
        writer.close()

def read_record(filename,compression_type='GZIP'):
    options = RECORD.TFRecordOptions(compression_type=compression_type)
    dataset = Loader.IterableDataset(filename,options=options)
    for d in dataset:
        string = str(decode_data(d),encoding='utf-8')
        print(string)
    dataset.close()

if __name__ == '__main__':
    write_record('./input.txt','./input.record')

    read_record('./input.record')