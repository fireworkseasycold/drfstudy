# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/7/30 10:28
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : urls.py
# @Software: PyCharm
from django.urls import path
from . import views

urlpatterns=[
    path("students/",views.StudentView.as_view()),
]