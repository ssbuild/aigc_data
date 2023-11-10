# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/11/9 15:51
import os
import sys
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../..')))

import copy
import json
import re
from data_sft_tools.utils.utils import format_parameters_from_json_string, get_type_from_desc
from data_sft_tools.qwen.tools_builder import ToolsBuilder
from data_sft_tools.base.tool_maker import ToolsDataMakerBase

# 下载数据集 https://github.com/tangqiaoyu/ToolAlpaca
class ToolsDataMaker(ToolsDataMakerBase):
    @classmethod
    def preprocess_tool_alpaca(cls,filename):
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
                    "value":  ToolsBuilder.build_final_response_with_args(instance["Final Thought"],instance["output"])
                })

                if conversations:
                    all_conversations.append({
                        "id": len(all_conversations),
                        "conversations": copy.deepcopy(conversations)
                    })
                conversations.clear()
        return all_conversations

    @classmethod
    def preprocess_tool_bench(cls, path_file):
        all_conversations = []
        if os.path.isdir(path_file):
            filenames = [os.path.join(path_file,f) for f in os.listdir(path_file) if f.endswith('.json')]
        else:
            filenames = [path_file]

        for index, filename in tqdm(enumerate(filenames), total=len(filenames)):
            with open(filename, mode='r', encoding='utf-8') as f:
                jd = json.loads(f.read())

            ag = jd["answer_generation"]
            if not ag["valid_data"]:
                continue

            query = ag["query"]
            finish_type = ag["finish_type"]
            final_answer = ag["final_answer"]
            function = ag["function"]
            train_messages = ag["train_messages"][-1]

            # assert finish_type == "give_answer"
            

            tools = []
            for func_obj in function:
                if func_obj["name"] == "Finish":
                    continue

                parameters_all = func_obj["parameters"]["properties"]
                required = func_obj["parameters"]
                parameters = {}
                for k, v in parameters_all.items():
                    parameters["name"] = k
                    parameters["description"] = v.get("description","")
                    parameters["required"] = k in required
                    parameters["schema"] = {}
                    parameters["type"] = v["type"]
                o = {
                    "name_for_human": func_obj["name"],
                    "name_for_model": func_obj["name"],
                    "description_for_model": func_obj["description"],
                    "parameters": parameters
                }
                tools.append(o)



            train_messages = [m for m in train_messages if m.get("valid",True) and m.get("role") != "system"]
            assert train_messages[0]["role"] == "user"
            assert "function_call" in train_messages[-1]
            train_messages[0]["content"] = query

            role = None
            for i, m in enumerate(train_messages):
                if m["role"] == role and role == "user":
                    assert ValueError(m["role"])
                role = m["role"]


            train_messages_parsed = []
            i = 0
            thought = ""
            while i < len(train_messages):
                m = train_messages[i]
                i += 1
                assert m["role"] in ["user", "function"]


                if m["role"] == "function":
                    assert train_messages_parsed[-1]["role"] == "assistant",ValueError(train_messages_parsed[-1])
                    train_messages_parsed[-1]["observation"] = m["content"]

                train_messages_parsed.append(m)
                m = train_messages[i]
                i += 1

                assert m["role"] == "assistant"
                function_call = None

                j = i - 1
                while j < len(train_messages):
                    m = train_messages[j]
                    if m["role"] != "assistant":
                        j -= 1
                        break
                    if "function_call" in m:
                        assert function_call is None
                        function_call = m["function_call"]
                    else:
                        thought += m["content"]
                    j += 1
                i = j
                i += 1

                assert function_call is not None
                train_messages_parsed.append({
                    "role" : "assistant",
                    "content": thought,
                    "function_call": function_call
                })

            conversations = []
            for i,(q,a) in enumerate(zip(train_messages_parsed[::2],train_messages_parsed[1::2])):
                role = q["role"]
                q = q["content"]
                thought = a["content"]
                function_call = a["function_call"]
                if i == 0:
                    conversations.append({
                        "from": "user",
                        "value": ToolsBuilder.build(tools, query=q)
                    })
                else:
                    assert role == "function"
                    conversations.append({
                        "from": "observation",
                        "value": q
                    })


                action = function_call["name"]
                action_input = function_call["arguments"]

                assert "observation" in a or (function_call["name"] == "Finish")

                if function_call["name"] == "Finish":
                    if finish_type == "give_answer":
                        try:
                            observation = json.loads(function_call["arguments"])["final_answer"]
                        except Exception as e:
                            # print(e)
                            conversations.pop(-1)
                            break
                    else:
                        conversations.pop(-1)
                        break
                    conversations.append({
                        "from": "assistant",
                        "value": ToolsBuilder.build_final_response_with_args(thought,observation)
                    })

                else:
                    observation = a["observation"]
                    response, observation = ToolsBuilder.build_response_with_args(thought,action,action_input,observation)
                    conversations.append({
                        "from": "assistant",
                        "value": response
                    })



            if conversations:
                all_conversations.append({
                    "id": len(all_conversations),
                    "conversations": copy.deepcopy(conversations)
                })



        return all_conversations



def build_tool_alpaca(filename,output_file):
    output_file_json = output_file.replace('.parquet', '.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    all_conversations = ToolsDataMaker.preprocess_tool_alpaca(filename)

    ToolsDataMaker.write(all_conversations, output_file)
    ToolsDataMaker.write_json(all_conversations, output_file_json)

    ToolsDataMaker.read(output_file)

def build_tool_bench(filename,output_file):
    output_file_json = output_file.replace('.parquet', '.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    all_conversations = ToolsDataMaker.preprocess_tool_bench(filename)

    ToolsDataMaker.write(all_conversations, output_file)
    ToolsDataMaker.write_json(all_conversations, output_file_json)

    ToolsDataMaker.read(output_file)

if __name__ == '__main__':
    build_tool_alpaca( r'F:\nlpdata_2023\ToolAlpaca\data\train_data.json',
                       r'F:\nlpdata_2023\ToolAlpaca\data\record\tool_alpaca_for_qwen.parquet')

    build_tool_bench(r'F:\nlpdata_2023\tool_bench\data\data\answer\G1_answer',
                     r'F:\nlpdata_2023\tool_bench\data\data\answer\tool_bench_g1_for_qwen.parquet')

    build_tool_bench(r'F:\nlpdata_2023\tool_bench\data\data\answer\G2_answer',
                     r'F:\nlpdata_2023\tool_bench\data\data\answer\tool_bench_g2_for_qwen.parquet')

    build_tool_bench(r'F:\nlpdata_2023\tool_bench\data\data\answer\G3_answer',
                     r'F:\nlpdata_2023\tool_bench\data\data\answer\tool_bench_g3_for_qwen.parquet')