# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/11/9 10:40
import copy
import json

class ToolsBuilder:

    TOOL_DESC = """Answer the following questions as best as you can. You have access to the following tools:"""

    @classmethod
    def build_system(cls,tools):
        if isinstance(tools, str):
            tools = json.loads(tools)
        prompt = copy.deepcopy(ToolsBuilder.TOOL_DESC)
        prompt += '\n' + json.dumps(tools,ensure_ascii=False,indent=4)
        return prompt


    @classmethod
    def build_response(cls,step):
        pos = step[0][2].find("Action Input: ")
        thought = step[0][2][:pos]
        action = step[0][0]
        action_input = step[0][1]

        pos = step[1].find("Response:") + len("Response:") + 1
        observation = step[1][pos:]

        response = thought + '\n' + f'<|assistant|>{action}\n'

        response += f'''
          ```python
        tool_call({action_input})
        ```
        '''


        return response,observation