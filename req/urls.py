# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/8/1 13:21
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : urls.py
# @Software: PyCharm
from django.urls import path

from . import views

urlpatterns=[
    path("students1/",views.StudentView.as_view()), #django视图类
    path("students/",views.StudentAPIView.as_view())  #drf视图类
]