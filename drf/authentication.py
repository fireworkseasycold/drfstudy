# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/8/17 17:38
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : aauthentication.py
# @Software: PyCharm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class ExampleAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        自定义认证方法
        :param request: 本地客户端发送过来的请求对象
        :return:
        """
        user = request.query_params.get("user")  # query_params覆盖GET
        # pwd = request.query_params.get("pwd")
        # if user != "root" or pwd != "root123456":  #密码不能带#,亲测路由会舍去# 这个类似于后门
        #     return None
        try:
            # get_user_model获取当前系统中用户表对象的用户模型类
            # suser = get_user_model().objects.first()
            user = get_user_model().objects.filter(username=user).first()
            # print("自定义Authentication通过认证：",user)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return (user, None) #按照固定格式返回（用户模型对象，None）
