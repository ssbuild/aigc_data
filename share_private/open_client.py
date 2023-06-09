# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/6/9 11:38
import os.path
import socket
import fastcrypto
import requests
from tqdm import tqdm
from fastdatasets.record import load_dataset as Loader,gfile,RECORD,DataType,BytesWriter
import fastcrypto
import pickle
import hashlib

# ,key,iv  length must 16
# aes 256
# key iv 元素取值范围 0-255  一共有 256 的 16次方 * 256 的 16次方 种秘钥

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


class DataReaderWriter:
    @staticmethod
    def md5(filename):
        with open(filename,mode='rb') as f:
            d = f.read()
        m = hashlib.md5()
        m.update(d)
        return (m.hexdigest())

    @staticmethod
    def write(data_meta, src_file, dst_file, compression_type='GZIP'):
        print('write', '==' * 30)
        # data_meta = {
        #     'dataset_name': 'test',
        #     'dataset_desc': '测试数据',
        #     'dataset_one_sample': '你是谁',
        #     'dataset_type': 'text',  # text , json , html , csv
        #     'dataset_count': 0,  # 会自动更新
        #     'dataset_hash': '',  # 会自动更新
        # }

        assert data_meta['dataset_type'] in ['text' , 'json' , 'html' , 'csv']

        num = 0
        with open(src_file, mode='r', encoding='utf-8', newline='\n') as f:
            lines = f.readlines()
            options = RECORD.TFRecordOptions(compression_type=compression_type)
            writer = BytesWriter(dst_file, options)
            for line in tqdm(lines, desc='write record'):
                if not line:
                    continue
                num += 1

                if num == 1:
                    data_meta['dataset_one_sample'] = line

                data = encode_data(bytes(line, encoding='utf-8'))
                writer.write(data)
            writer.close()

        hash = DataReaderWriter.md5(dst_file)
        data_meta['dataset_count'] = num
        data_meta['dataset_hash'] = hash
        # meta_file = dst_file + '.meta'
        # with open(meta_file,mode='wb') as f:
        #     pickle.dump(data_meta,f)

    @staticmethod
    def read(filename,limit = 10, compression_type='GZIP'):
        print('read','==' * 30)
        options = RECORD.TFRecordOptions(compression_type=compression_type)
        dataset = Loader.IterableDataset(filename, options=options)
        for i,d in enumerate(dataset):
            if i >= limit:
                break
            string = str(decode_data(d), encoding='utf-8')
            print(string)
        dataset.close()

class OpenDataCient:
    def __init__(self,user):
        assert isinstance(user,str)
        assert len(user) > 0

        ip = self._resolve_domain('tx.ssdog.cn')
        assert len(ip) > 0
        self.ip = ip[0]
        self.port = 8088
        self.user = user

        self._token_url = 'http://{}:{}/get_token'.format(self.ip, self.port)
        self._push_dataset_url = 'http://{}:{}/push_dataset'.format(self.ip, self.port)
        self._pull_dataset_url = 'http://{}:{}/pull_dataset'.format(self.ip, self.port)
        self._list_dataset_url = 'http://{}:{}/list_dataset'.format(self.ip, self.port)

    def _resolve_domain(self,domain):
        ip_list = []
        try:
            addrs = socket.getaddrinfo(domain, None)
            for addr in addrs:
                ip = addr[4][0]
                ip_list.append(ip)
        except Exception as e:
            print(e)
        return ip_list

    # 注册token ， 如果绑定的用户已存在，返回绑定的token ， 否则生成新token
    def get_token(self):
        data = {
            'user': self.user
        }
        r = requests.post(self._token_url, data=data)
        r = r.json()
        token = r['result']
        return token

    def push_dataset(self,token,**kwargs):
        assert len(kwargs)
        data = {
            'user': self.user,
            'token': token,
             **kwargs
        }
        r = requests.post(self._push_dataset_url, data=data)
        r = r.json()
        if r['code'] != 0:
            return None
        return 0

    def pull_dataset(self,token, dataset_name):
        if not isinstance(dataset_name,list):
            dataset_name = [dataset_name]
        data = {
            'user': self.user,
            'token': token,
            'dataset_name': dataset_name,
        }
        r = requests.post(self._pull_dataset_url, data=data)
        r = r.json()
        if r['code'] != 0:
            return None
        return r['result']

    def list_dataset(self,token):
        data = {
            'user': self.user,
            'token': token,
        }
        r = requests.post(self._list_dataset_url, data=data)
        r = r.json()
        if r['code'] != 0:
            return None
        return r['result']

