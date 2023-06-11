# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/6/8 10:43

from tqdm import tqdm
from fastdatasets.record import load_dataset as Loader,gfile,RECORD,DataType,BytesWriter
import fastcrypto
import pickle
import hashlib

global_args = {
    "key":  bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]),
    "iv" : bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
}


class Encrypt:
    @staticmethod
    def encode_data(data: bytes,key=global_args['key'],iv=global_args['iv']):
        ret = fastcrypto.aes_encode(data, key, iv)
        assert ret[0] == 0
        crypt_data = ret[1]
        return crypt_data

    @staticmethod
    def decode_data(data: bytes,key=global_args['key'],iv=global_args['iv']):
        ret = fastcrypto.aes_decode(data, key, iv)
        assert ret[0] == 0
        return ret[1]

    @staticmethod
    def hash_md5(d):
        m = hashlib.md5()
        m.update(d)
        return m.hexdigest()



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
        #     'dataset_count': 0,  # 自动更新
        #     'dataset_hash': '',  # 自动更新
        #     'key': bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]), # 自动更新
        #     'iv': bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]),, # 自动更新
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
        data_meta['key'] = global_args['key']
        data_meta['iv'] = global_args['iv']

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





if __name__ == '__main__':

    data_meta = {
        'dataset_name': "test",
        'dataset_desc': "test",
        'dataset_type':  "text" , # text , json , html , csv
        'dataset_one_sample': '',  # 会自动更新
        'dataset_hash': '',  # 会自动更新
        'key': global_args['key'],  # 自动更新
        'iv': global_args['iv'],  # 自动更新
    }

    input_file = './input.txt'
    output_file = './outputs/output.record'
    DataReaderWriter.write(data_meta,input_file,output_file )
    # 查看前10条
    DataReaderWriter.read(output_file, limit=10)

    print(data_meta)
