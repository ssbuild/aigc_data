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
    def write(src_file, dst_file, compression_type='GZIP'):
        print('\n' * 3,'write', '==' * 30,'\n' * 3,)



        num = 0
        with open(src_file, mode='r', encoding='utf-8', newline='\n') as f:
            lines = f.readlines()
            options = RECORD.TFRecordOptions(compression_type=compression_type)
            writer = BytesWriter(dst_file, options)
            for line in tqdm(lines, desc='write record'):
                if not line:
                    continue
                num += 1
                data = Encrypt.encode_data(bytes(line, encoding='utf-8'))
                writer.write(data)
            writer.close()

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
    input_file = '../../assets/input.txt'
    output_file = '../../assets/outputs/output.record'
    DataReaderWriter.write(input_file,output_file )
    # 查看前10条
    DataReaderWriter.read(output_file, limit=10)

