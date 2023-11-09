# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/11/9 15:56
import json
import re

text = "Send an HTTP request with the specified method, headers, and data to the Httpbin API for testing purposes.\nParameters: {\"method\": \"Required. string. One of: [GET, POST, PUT, DELETE, HEAD, PATCH]. The HTTP method to use (GET, POST, PUT, DELETE, HEAD, or PATCH).\", \"url\": \"Required. string. The endpoint URL to send the request to.\", \"headers\": \"Object.  A key-value pair of headers to include in the request.\", \"data\": \"Object.  A key-value pair of data to include in the request body.\"}\nOutput: Successful response.\n - Format: application/json\n - Structure: Object{response: Object{status_code, headers: Object, body}}"


result = re.match(r".*Parameters: (.*)Output",text,flags=re.DOTALL )

print(result)


print(result.group(1))

print(json.loads(result.group(1)))