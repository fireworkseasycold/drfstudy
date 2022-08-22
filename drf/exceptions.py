# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/8/19 8:37
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : excepition.py
# @Software: PyCharm
from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.db import DataError


#写完后要配置
def my_exception_handler(exc,context):
    """自定义异常函数
    :exc 本次发生的异常情况
    :context 本次发生异常时的上下文环境信息,字典
    """
    #先让drf把自己能处理的异常处理
    response=exception_handler(exc,context)
    if response is None:
        """当前发生的异常,drf无法处理,则编写自己的异常处理"""
        if isinstance(exc,ZeroDivisionError):
            response=Response({'detail':"0不能作为除数"})

        if isinstance(exc,DataError):
            response=Response({'detail':'数据存储异常!'})
    return response
