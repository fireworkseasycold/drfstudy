# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/8/18 9:21
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : permissions.py
# @Software: PyCharm

from rest_framework.permissions import BasePermission
class ExamplePermission(BasePermission):
    # def has_permission(self, request, view):
    #     """
    #     自定义视图权限
    #     :param request: 本次客户端提交的请求对象
    #     :param view: 本次客户端访问的视图类
    #     :return: True表示允许访问视图类
    #     """
    #     return bool(request.user and request.user.username=='xl')

    def has_object_permission(self, request, view,obj):
        from school.models import Student
        if isinstance(obj,Student):
            #限制只有xl才能操作Student模型
            user=request.query_params.get("user")
            return user == 'root'
        else:
            #操作其他模型，直接放行
            return True
