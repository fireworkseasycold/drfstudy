# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/8/16 15:17
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : urls.py
# @Software: PyCharm
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register('students',views.StudentModelViewSet,basename="students")
urlpatterns=[
]+router.urls