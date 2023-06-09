# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/6/9 11:38
import base64
import copy
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

class Encrypt:
    @staticmethod
    def encode_data(data: bytes,key=key,iv=iv):
        ret = fastcrypto.aes_encode(data, key, iv)
        assert ret[0] == 0
        crypt_data = ret[1]
        return crypt_data

    @staticmethod
    def decode_data(data: bytes,key=key,iv=iv):
        ret = fastcrypto.aes_decode(data, key, iv)
        assert ret[0] == 0
        return ret[1]

    @staticmethod
    def hash_md5(d):
        m = hashlib.md5()
        m.update(d)
        return (m.hexdigest())

    @staticmethod
    def encode_password(password):
        key = bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        iv = bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        password = Encrypt.hash_md5(Encrypt.encode_data(bytes(password,encoding='utf-8'), key=key, iv=iv))
        password = bytes(password,encoding='utf-8')
        password = base64.b64encode(password)
        password = str(password,encoding='utf-8')
        return password

class DataReaderWriter:
    @staticmethod
    def md5(filename):
        with open(filename,mode='rb') as f:
            d = f.read()
        return Encrypt.hash_md5(d)

    @staticmethod
    def write(data_meta, src_file, dst_file, compression_type='GZIP'):
        print('\n' * 3,'write', '==' * 30,'\n' * 3,)
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

                data = Encrypt.encode_data(bytes(line, encoding='utf-8'))
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
        print('\n' * 3,'read','==' * 30,'\n' * 3,)
        options = RECORD.TFRecordOptions(compression_type=compression_type)
        dataset = Loader.IterableDataset(filename, options=options)
        for i,d in enumerate(dataset):
            if i >= limit:
                break
            string = str(Encrypt.decode_data(d), encoding='utf-8')
            print(string)
        dataset.close()




class OpenDataCient:
    def __init__(self,user_info):
        self.user_info = copy.deepcopy(user_info)
        password = self.user_info['password']
        password = Encrypt.encode_password(password)
        self.user_info['password'] = password
        print('\n' * 3,'*** user info ***','\n',self.user_info,'\n' * 3)
        ip = self._resolve_domain('tx.ssdog.cn')
        assert len(ip) > 0
        self.ip = ip[0]
        self.port = 8088

        self._token_url = 'http://{}:{}/get_token'.format(self.ip, self.port)
        self._push_dataset_url = 'http://{}:{}/push_dataset'.format(self.ip, self.port)
        self._pull_dataset_url = 'http://{}:{}/pull_dataset'.format(self.ip, self.port)
        self._list_dataset_url = 'http://{}:{}/list_dataset'.format(self.ip, self.port)

        self._token = None

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

    # 认证成功获取token
    def auth(self):
        data = {
            **self.user_info,
        }
        r = requests.post(self._token_url, data=data)
        r = r.json()
        token = r['result']
        return token

    def push_dataset(self,**kwargs):
        assert len(kwargs)
        data = {
            **self.user_info,
            'token': self._token,
             **kwargs
        }
        r = requests.post(self._push_dataset_url, data=data)
        r = r.json()
        if r['code'] != 0:
            return None
        return 0

    def pull_dataset(self, dataset_name):
        if not isinstance(dataset_name,list):
            dataset_name = [dataset_name]
        data = {
             **self.user_info,
            'token': self._token,
            'dataset_name': dataset_name,
        }
        r = requests.post(self._pull_dataset_url, data=data)
        r = r.json()
        if r['code'] != 0:
            return None
        return r['result']

    def list_dataset(self):
        data = {
             **self.user_info,
            'token': self._token,
        }
        r = requests.post(self._list_dataset_url, data=data)
        r = r.json()
        if r['code'] != 0:
            return None
        return r['result']

