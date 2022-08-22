# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/7/30 7:50
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : serializers.py
# @Software: PyCharm
#新建序列化器serializers.py
from rest_framework import serializers
from stu_api.models import Student

#创建序列化器类，回头会在视图中被调用，用于序列化与反序列化
class StudentExampleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields="__all__"  #决定序列化里给客户端提供的字段，all代表所有
        # fields=["id","name"] #只给两个