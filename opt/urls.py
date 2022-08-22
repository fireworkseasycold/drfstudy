# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/8/17 14:35
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : urls.py
# @Software: PyCharm
from django.urls import path, re_path

from . import views

urlpatterns=[
    path("example/",views.ExampleView.as_view()),
    re_path("^permission/(?P<pk>\d+)$",views.ExampleView2.as_view()),
    path("filter/",views.ExampleView3.as_view()),
    path("demopaginate/",views.ExampleView4.as_view()),
    path("except/",views.ExampleView5.as_view()),
]