# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/7/29 10:00
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : urls.py
# @Software: PyCharm
from django.urls import path, re_path
from . import views

urlpatterns = [
    path("students/", views.StudentView.as_view()),
    re_path("students/(?P<pk>\d+)/$", views.StudentInfoView.as_view()),
]
