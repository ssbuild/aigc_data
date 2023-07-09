# -*- coding: utf-8 -*-
# @Time:  16:34
# @Author: tk
# @File：make_parquet_dataset

# -*- coding: utf-8 -*-
# @Time:  22:31
# @Author: tk
# @File：make_dataset
import json
import os
from fastdatasets.parquet.writer import PythonWriter
from fastdatasets.parquet.dataset import load_dataset,arrow
from fastdatasets import gfile
from tqdm import tqdm

with_stream = True



class DataWriter:
    def get_file_data(self,in_files):
        all_data = []
        for file in in_files:
            with open(file, mode='r', encoding='utf-8') as f:
                jds = json.loads(f.read())
                all_data.append((os.path.basename(file), jds))
        return all_data

    @classmethod
    def get_split_filename(cls,filename,split):
        if split == 1:
            return [filename]
        f1 = os.path.dirname(filename)
        f2 = os.path.basename(filename)
        f2 = f2.rsplit('.',maxsplit=1)
        return [os.path.join(f1,f2[0] + '_part{}.'.format(i) + f2[1]) for i in range(split)]

    #建议切分 每个文件小于 1G
    def write(self,in_files,outfile,split=1):
        all_data = self.get_file_data(in_files)

        total = [len(_[1]) for _ in all_data]
        total = sum(total)
        limit_n = total // split
        limit_n += total % split
        print(total,limit_n)
        outfiles = self.get_split_filename(outfile,split)
        fs = [PythonWriter(outfiles[_], schema=schema) for _ in range(split)]
        N = 10000

        data_index = -1
        file_index = -1
        for file, jds in all_data:
            batch = {k: [] for k in schema}
            for i, jd in enumerate(tqdm(jds)):
                data_index += 1
                if data_index % limit_n == 0:
                    file_index += 1
                idx = jd.pop('id',None)
                if isinstance(idx,str):
                    idx = int(idx)
                if idx is None:
                    idx = i
                batch["id"].append(idx)

                for k, v in jd.items():
                    batch[k].append(v)

                if len(batch["id"]) % N == 0:
                    status = fs[file_index].write_batch(batch.keys(), batch.values())
                    assert status.ok(), status.message()
                    for k, v in batch.items():
                        v.clear()
            if len(batch["id"]):
                status = fs[file_index].write_batch(batch.keys(), batch.values())
                assert status.ok(), status.message()
                for k, v in batch.items():
                    v.clear()

        [_.close() for _ in fs]

    @staticmethod
    def read(file, split=1):
        file = DataWriter.get_split_filename(file,split=split)
        dataset = load_dataset.RandomDataset(file,with_share_memory=not with_stream)
        print(file,'total', len(dataset))
        for i in range(len(dataset)):
            print(dataset[i])
            if i > 2:
                break


def make_data(patten,split=1):
    fs_list = gfile.glob(patten)
    in_files = [
        ([f],os.path.join(os.path.dirname(f),os.path.basename(f).replace('.json','.parquet'))) for f in fs_list
    ]
    for files, outfile in in_files:
        DataWriter().write(files, outfile,split=split)
        DataWriter.read(outfile,split=split)

if __name__ == '__main__':
    schema = {
        'id': 'int32',
        'prefix': 'str',
        'num_turns': 'int32',
        'plain_text': 'str',
    }
    base_dir = r'D:\tmp_dataset\moss_sft_002'
    make_data(gfile.glob(os.path.join(base_dir, '*.json')), split=1)

