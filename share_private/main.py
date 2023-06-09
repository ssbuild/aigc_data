# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/6/8 10:43

import argparse
import os.path

from open_client import DataReaderWriter,OpenDataCient
parser = argparse.ArgumentParser(description='')

parser.add_argument('--input', type=str,default=None ,help='输入文件路径')
parser.add_argument('--output', type=str,default=None, help='输出文件路径')
parser.add_argument('--user', type=str,default="", help='用户名')
parser.add_argument('--method', type=str,default='', help='one of upload download list query or empty')
parser.add_argument('--dataset_name', type=str,default='', help='dataset_name')
parser.add_argument('--dataset_desc', type=str,default='', help='')
parser.add_argument('--dataset_type', type=str,default='', help='')

args = parser.parse_args()

def make_dataset(args):
    data_meta = {
        'dataset_name': args.dataset_name,
        'dataset_desc': '测试数据',
        'dataset_type': 'text',  # text , json , html , csv
        'dataset_one_sample': '',  # 会自动更新
        'dataset_count': 0,  # 会自动更新
        'dataset_hash': '',  # 会自动更新
    }

    input_file = args.input
    output_file = args.output

    outdir = os.path.dirname(output_file)
    if not os.path.exists(os.path.dirname(outdir)):
        os.mkdir(outdir)
    DataReaderWriter.write(data_meta, input_file, output_file)
    # 查看前10条
    DataReaderWriter.read(output_file, limit=10)
    return data_meta


if __name__ == '__main__':

    args = parser.parse_args()
    #制作数据
    data_meta = None
    if args.input:
        data_meta = make_dataset(args)



    if args.user:
        uClient = OpenDataCient(user=args.user)

        # 获取id
        token_uuid = uClient.get_token()

        #upload download list query
        if args.method == 'upload':
            assert data_meta is not None
            # 上传
            uClient.push_dataset(token_uuid,**data_meta)

        elif args.method == 'download':
            # 获取其他数据集信息
            new_data_meta = uClient.pull_dataset(token_uuid, dataset_name=args.dataset_name)
            print(new_data_meta)
        elif args.method == 'list':
            # 查看列表
            print(uClient.list_dataset(token_uuid))

