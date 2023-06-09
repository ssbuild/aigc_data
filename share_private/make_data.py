# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/6/8 10:43

from open_client import DataReaderWriter,OpenDataCient





def make_dataset():
    data_meta = {
        'dataset_name': 'test',
        'dataset_desc': '测试数据',
        'dataset_type': 'text',  # text , json , html , csv
        'dataset_column': '',  # json or csv 列  逗号 分割
        'dataset_one_sample': '',  # 会自动更新
        'dataset_count': 0,  # 会自动更新
        'dataset_hash': '',  # 会自动更新
    }

    DataReaderWriter.write(data_meta, './input.txt', './input.record')


    # 查看前10条
    DataReaderWriter.read('./input.record', limit=10)

    return data_meta


if __name__ == '__main__':
    #制作数据
    data_meta = make_dataset()

    print(data_meta)

    # #上传信息
    # upClient = OpenDataCient(user='default')
    #
    # ## 获取id
    # token_uuid = upClient.new_token()
    #
    # # 上传信息
    # upClient.pull_dataset(token_uuid,**data_meta)
    #
    #
    #
    # # 查看列表
    # print(upClient.list_dataset(token_uuid))
    #
    # # 获取其他数据集信息
    # new_data_meta = upClient.pull_dataset(token_uuid,dataset_name='test')
