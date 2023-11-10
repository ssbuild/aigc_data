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
        tools_str = json.dumps(tools, ensure_ascii=False, indent=4)
        if not tools_str.startswith('\n'):
            tools_str = '\n' + tools_str
        prompt += tools_str
        return prompt


    @classmethod
    def build_response(cls,step):

        pos = step[0][2].find("\nAction: ")
        thought = step[0][2][:pos]
        action = step[0][0]
        action_input = step[0][1]

        # pos = step[1].find("Response:") + len("Response:") + 1
        # observation = step[1][pos:]
        observation = step[1]

        response = thought + '\n' + f'<|assistant|>{action}\n'

        response += f'''
          ```python
        tool_call({action_input})
        ```
        '''


        return response,observation