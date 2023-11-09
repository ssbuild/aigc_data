# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/11/9 15:51

# 下载数据集 https://github.com/tangqiaoyu/ToolAlpaca

import json
import os.path
import re
import sys
sys.path.append('.')


from utils import format_parameters_from_json_string, get_type_from_desc
from data_tools import ToolsBuilder
from fastdatasets.parquet.writer import PythonWriter



with_stream = True
class ToolsDataMaker:
    @classmethod
    def preprocess(cls,filename):
        with open(filename, mode='r', encoding='utf-8') as f:
            jds = json.loads(f.read())

        all_conversations = []
        for jd in jds:
            Function_Description = jd["Function_Description"]
            Instances = jd["Instances"]

            tools = []
            conversations = []
            error = False
            for func_name,func_description in Function_Description.items():
                if func_name == "components":
                    continue

                try:
                    parameters_all = re.match(r".*Parameters: (.*)\nOutput", func_description, flags=re.DOTALL).group(1)
                    parameters_all = format_parameters_from_json_string(parameters_all)
                    func_desc = re.match(r"(.*)\nParameters", func_description, flags=re.DOTALL)
                    func_desc = func_desc.group(1) if func_desc else ""
                    parameters = {}
                    for k, v in parameters_all.items():
                        parameters["name"] = k
                        parameters["description"] = v
                        parameters["required"] = 'Required' in v
                        parameters["schema"] = {}
                        parameters["type"] = get_type_from_desc(v)
                    o = {
                        "name_for_human": func_name,
                        "name_for_model": func_name,
                        "description_for_model": func_desc,
                        "parameters": parameters
                    }
                    tools.append(o)
                except Exception as e:
                    print(func_name,func_description)
                    print('***parameters_all',parameters_all)
                    error = True
                    raise e
            if error:
                continue
            inst_id = -1
            for instance in Instances:
                inst_id += 1
                intermediate_steps = instance.get("intermediate_steps",None)
                if not intermediate_steps:
                    continue
                if len(intermediate_steps) > 5:
                    continue

                if len(intermediate_steps) != 1:
                    # qwen 模板暂时不支持同时请求多个函数
                    continue
                conversations.append({
                    "role": "user",
                    "content": ToolsBuilder.build(tools,query=instance["input"])
                })

                response,observation = ToolsBuilder.build_response(intermediate_steps[0])
                conversations.append({
                    "role": "assistant",
                    "content": response
                })

                conversations.append({
                    "role": "observation",
                    "content": 'Observation: ' + observation
                })

                conversations.append({
                    "role": "assistant",
                    "content":  instance["output"]
                })

            all_conversations.append({
                "id": len(all_conversations),
                "conversations": conversations
            })
        return all_conversations

    @classmethod
    def write(cls,all_conversations,outfile):
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
        with open(outfile,mode='w',encoding='utf-8') as f:
            for conversations in all_conversations:
                f.write(json.dumps(conversations,ensure_ascii=False) + '\n')


    @staticmethod
    def read(file):
        from fastdatasets.parquet.dataset import load_dataset
        dataset = load_dataset.RandomDataset(file, with_share_memory=not with_stream)
        print(file, 'total', len(dataset))
        for i in range(len(dataset)):
            print(dataset[i])
            break

if __name__ == '__main__':
    filename = r'E:\py-http\ToolAlpaca\data\train_data.json'
    output_file = r'E:\py-http\ToolAlpaca\data\record\qwen_tools.parquet'
    output_file_json = r'E:\py-http\ToolAlpaca\data\record\qwen_tools.json'
    os.makedirs(os.path.dirname(output_file),exist_ok=True)

    all_conversations = ToolsDataMaker.preprocess(filename)

    ToolsDataMaker.write(all_conversations,output_file)
    ToolsDataMaker.write_json(all_conversations,output_file_json)

    ToolsDataMaker.read(output_file)
