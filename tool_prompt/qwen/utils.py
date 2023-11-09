# coding=utf8
# @Time    : 2023/11/9 20:17
# @Author  : tk
# @FileName: utils
import json


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
    return 'object'
    raise ValueError(desc)



def clean_json(json_str):
    new_list = []
    for _ in json_str.split(', '):
        if ":" in _:
            new_list.append(_)
        else:
            new_list.append(_.replace('"', "") + '')
    json_str = ', '.join(new_list)
    new_list = []
    for _ in json_str.split(', "'):
        if not _.endswith('"') and not _.endswith('}') and not _.endswith('\n'):
            _ += '"'
        new_list.append(_)
    json_str = ', "'.join(new_list)
    if json_str.endswith('.}'):
        json_str = json_str[:-2] + '."}'
    return json_str
def format_parameters_from_json_string(json_str: str):
    #{"name": "Required. string.", "method": "Required. string. One of: [GET, POST, PUT, DELETE].", "url": "Required. string.", "response": "Required. #MockAPIResponseInput"}
    try:
        return json.loads(json_str)
    except:
        try:
            json_str_new = clean_json(json_str)
            return json.loads(json_str_new)
        except  Exception as e:
            raise e