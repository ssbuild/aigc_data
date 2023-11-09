# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/11/9 15:51

# 下载数据集 https://github.com/tangqiaoyu/ToolAlpaca

import json
import re
import sys
import trace

sys.path.append('.')
from data_tools import ToolsBuilder


# 调试中。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。

RESPONSE_PROMPT = """Thought: {prompt_desc}。
Action: {action}
Action Input: {action_input}"""
def get_type_from_desc(desc):
    desc = desc.lower()
    if 'string.' in desc:
        return "string"
    if 'integer.' in desc:
        return "integer"
    if 'number.' in desc:
        return "number"
    if 'boolean.' in desc:
        return "boolean"
    if 'array.' in desc :
        return "array"
    if 'array[' in desc :
        return "array"
    if 'object.' in desc:
        return "object"
    raise ValueError(desc)



def format_parameters_from_json_string(json_str: str):
    #{"name": "Required. string.", "method": "Required. string. One of: [GET, POST, PUT, DELETE].", "url": "Required. string.", "response": "Required. #MockAPIResponseInput"}

    kv_list = json_str.split(',')
    kv_list_ = []
    for kv in kv_list:
        if kv.find(':') != -1:
            kv = kv.split(':',maxsplit=1)
            tmp = kv[1].strip()
            pos = tmp.rfind('"}')
            kv = kv[0] + ": " + tmp[0] + tmp[1:pos].replace('"','“') + tmp[pos:]
        else:
            kv = kv.replace('"', '“')
        kv_list_.append(kv)

    json_str = ','.join(kv_list_)
    try:
        return json.loads(json_str)
    except Exception as e:
        raise e
def make_qwen_tool(filename):


    with open(filename, mode='r', encoding='utf-8') as f:
        jds = json.loads(f.read())

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
                parameters_all = re.match(r".*Parameters: (.*)Output", func_description, flags=re.DOTALL).group(1)
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
                # print(json.dumps(o,ensure_ascii=False,indent=2))
            except Exception as e:
                print('*' * 30)
                print(func_name,func_description)
                print('***parameters_all',parameters_all)
                raise e
                error = True
        if error:
            continue
        inst_id = -1
        for instance in Instances:
            inst_id += 1
            if not instance.get("intermediate_steps"):
                continue
            if len(instance["intermediate_steps"]) > 5:
                continue

            print(len(instance["intermediate_steps"]))
            if inst_id == 0:
                conversations.append({
                    "role": "user",
                    "q": ToolsBuilder.build(tools,query=instance["input"])
                })
            # for step in instance["intermediate_steps"]:
            #     # RESPONSE_PROMPT
            #     conversations.append({
            #         "role": "user",
            #         "q": instance["input"]
            #     })

if __name__ == '__main__':
    filename = r'E:\py-http\ToolAlpaca\data\train_data.json'

    make_qwen_tool(filename)