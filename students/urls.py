# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/7/30 7:56
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : URLS.py
# @Software: PyCharm
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("students2", views.StudentModelViewSet, basename="students2")  # 有几个写几个

#路由列表
urlpatterns = [

] + router.urls

