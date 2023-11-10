# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/11/9 15:51
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../..')))

import copy
import json
import re
from data_tools.utils.utils import format_parameters_from_json_string, get_type_from_desc
from data_tools.qwen.tools_builder import ToolsBuilder
from data_tools.base.tool_maker import ToolsDataMakerBase

# 下载数据集 https://github.com/tangqiaoyu/ToolAlpaca
class ToolsDataMaker(ToolsDataMakerBase):
    @classmethod
    def preprocess(cls,filename):
        with open(filename, mode='r', encoding='utf-8') as f:
            jds = json.loads(f.read())

        all_conversations = []
        for jd in jds:
            Function_Description = jd["Function_Description"]
            Instances = jd["Instances"]

            tools = []
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

            conversations = []
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
                    "from": "user",
                    "value": ToolsBuilder.build(tools,query=instance["input"])
                })

                response,observation = ToolsBuilder.build_response(intermediate_steps[0])
                conversations.append({
                    "from": "assistant",
                    "value": response
                })

                conversations.append({
                    "from": "observation",
                    "value": 'Observation: ' + observation
                })

                conversations.append({
                    "from": "assistant",
                    "value":  instance["output"]
                })

                if conversations:
                    all_conversations.append({
                        "id": len(all_conversations),
                        "conversations": copy.deepcopy(conversations)
                    })
                conversations.clear()
        return all_conversations




if __name__ == '__main__':
    filename = r'E:\py-http\ToolAlpaca\data\train_data.json'
    output_file = r'E:\py-http\ToolAlpaca\data\record\tool_alpaca_for_qwen.parquet'
    output_file_json = r'E:\py-http\ToolAlpaca\data\record\tool_alpaca_for_qwen.json'
    os.makedirs(os.path.dirname(output_file),exist_ok=True)

    all_conversations = ToolsDataMaker.preprocess(filename)

    ToolsDataMaker.write(all_conversations,output_file)
    ToolsDataMaker.write_json(all_conversations,output_file_json)

    ToolsDataMaker.read(output_file)
