# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/11/10 9:06
import json
from fastdatasets.parquet import PythonWriter


class ToolsDataMakerBase:

    @classmethod
    def write(cls, all_conversations, outfile):
        schema = {
            'id': 'int32',
            'conversations': 'map_list',
        }

        fs = PythonWriter(outfile, schema=schema)
        N = 1000

        batch = {k: [] for k in schema}
        for conversations in all_conversations:

            batch["id"].append(conversations["id"])
            batch["conversations"].append(conversations["conversations"])

            if len(batch["id"]) % N == 0:
                status = fs.write_batch(batch.keys(), batch.values())
                assert status.ok(), status.message()
                for k, v in batch.items():
                    v.clear()
        if len(batch["id"]):
            status = fs.write_batch(batch.keys(), batch.values())
            assert status.ok(), status.message()
            for k, v in batch.items():
                v.clear()

        fs.close()
    @classmethod
    def write_json(cls, all_conversations, outfile):
        with open(outfile, mode='w', encoding='utf-8') as f:
            for conversations in all_conversations:
                f.write(json.dumps(conversations, ensure_ascii=False) + '\n')

    @staticmethod
    def read(file,n = 1,with_stream = True):
        from fastdatasets.parquet.dataset import load_dataset
        dataset = load_dataset.RandomDataset(file, with_share_memory=not with_stream)
        print(file, 'total', len(dataset))
        for i in range(len(dataset)):
            if i >= n:
                break
            print(json.dumps(dataset[i],ensure_ascii=False,indent=2))
