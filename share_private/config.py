# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/6/9 14:30



user_info = {
    "user": "admin",
    "password": "~!@~!~123456"
}


# 加密key

# ,key,iv  length must 16
# aes 256
# key iv 元素取值范围 0-255  一共有 256 的 16次方 * 256 的 16次方种秘钥


global_args = {
    "key":  bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]),
    "iv" : bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
}