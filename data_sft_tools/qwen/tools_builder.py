# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/11/9 10:40
import json

class ToolsBuilder:
    TOOL_DESC = """{name_for_model}: Call this tool to interact with the {name_for_human} API. What is the {name_for_human} API useful for? {description_for_model} Parameters: {parameters} Format the arguments as a JSON object."""

    REACT_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

{tool_descs}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {query}"""

    @classmethod
    def build(cls,tools,query):
        if isinstance(tools, str):
            tools = json.loads(tools)
        TOOL_DESC = ToolsBuilder.TOOL_DESC
        REACT_PROMPT = ToolsBuilder.REACT_PROMPT
        tool_descs = []
        tool_names = []
        for info in tools:
            tool_descs.append(
                TOOL_DESC.format(
                    name_for_model=info['name_for_model'],
                    name_for_human=info['name_for_human'],
                    description_for_model=info['description_for_model'],
                    parameters=json.dumps(
                        info['parameters'], ensure_ascii=False),
                )
            )
            tool_names.append(info['name_for_model'])
        tool_descs = '\n\n'.join(tool_descs)
        tool_names = ','.join(tool_names)

        prompt = REACT_PROMPT.format(tool_descs=tool_descs, tool_names=tool_names, query=query)
        return prompt


    @classmethod
    def build_response(cls,step):
        pos = step[0][2].find("\nAction:")
        thought = step[0][2][:pos]
        action = step[0][0]
        action_input = step[0][1]

        # pos = step[1].find("Response:") + len("Response:") + 1
        # observation = step[1][pos:]
        observation = step[1]
        response = f"""
Thought: {thought}
Action: {action}
Action Input: {action_input}
Observation: {observation}
"""
        return response,observation

    @classmethod
    def build_response_with_args(cls,thought, action,action_input,observation):
        response = f"""
Thought: {thought}
Action: {action}
Action Input: {action_input}
Observation: {observation}
"""
        return response, observation

    @classmethod
    def build_final_response_with_args(cls, thought, final_answer):
        response = f"""
Thought: {thought}
Final Answer: {final_answer}
"""
        return response