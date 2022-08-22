# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/8/1 16:46
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from stu_api.models import Student


class StudentModelSerializer(serializers.ModelSerializer):  #注意一定是ModelSerializer而不是Serializer，否则，会发现serializer.data={}
    class Meta:
        model=Student
        fields="__all__"  #决定序列化里给客户端提供的字段，all代表所有
        extra_kwargs = {
            "age": {
                "min_value": 5,
                "max_value": 20,
                "error_messages": {
                    "min_value": "年龄的最小值必须大于等于5",
                    "max_value": "年龄的最大值必须小于等于20",
                },
            },
        }

class Student2ModelSerializer(
    serializers.ModelSerializer):  # 注意一定是ModelSerializer而不是Serializer，否则，会发现serializer.data={}
    class Meta:
        model = Student
        fields = "__all__"  # 决定序列化里给客户端提供的字段，all代表所有
        extra_kwargs = {
            "age": {
                "min_value": 5,
                "max_value": 20,
                "error_messages": {
                    "min_value": "年龄的最小值必须大于等于5",
                    "max_value": "年龄的最大值必须小于等于20",
                },
            },
        }