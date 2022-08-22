# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/8/1 16:35
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : urls.py
# @Software: PyCharm
from django.urls import path,re_path
from django.utils import timezone

from . import views

urlpatterns=[
    path("students/",views.StudentAPIView.as_view()),
    re_path("^students/(?P<pk>\d+)/$",views.StudentInfoAPI.as_view()),
    #GenericAPIView通用视图类（其实是把上方的基础视图类使用drf的进一步封装了）
    path("students2/",views.StudentGenericAPIView.as_view()),
    re_path("^students2/(?P<pk>\d+)/$",views.StudentInfoGenericAPIView.as_view()),
    #GenericAPIView+mixins 通用视图类+模型扩展类
    path("students3/",views.StudentMixinView.as_view()),
    re_path("^students3/(?P<pk>\d+)/$",views.StudentInfoMixinView.as_view()),
    #视图子类
    path("students4/",views.StudentView.as_view()),
    re_path("^students4/(?P<pk>\d+)/$",views.StudentInfoView.as_view()),
    #基本视图集
    path("students5/",views.StudentViewSet.as_view({
        'get': 'get_list',  #视图类方法，可以是原来的http请求动作，也可以是自定义的方法名
        'post': 'post',
    })),  #视图集ViewSet重写了as_view,{"http请求动作":"视图方法"}，asview源码里循环setattr(视图类对象, HTTP请求动作, 函数)
    re_path("^students5/(?P<pk>\d+)/$",views.StudentViewSet.as_view({
        'get':'get_student_info',
        'put':'update_student_info',
        'delete':'delete_student_info',
    })),
    #GenericViewSet通用视图集
    path("students6/",views.StudentGenericViewSet.as_view({
        'get': 'list',  #视图类方法，可以是原来的http请求动作，也可以是自定义的方法名
        'post': 'create',
    })),  #视图集ViewSet重写了as_view,{"http请求动作":"视图方法"}，asview源码里循环setattr(视图类对象, HTTP请求动作, 函数)
    re_path("^students6/(?P<pk>\d+)/$",views.StudentGenericViewSet.as_view({
        'get':'get_student_info',
        'put':'update_student_info',
        'delete':'delete_student_info',
    })),
    #GenericViewSet通用视图集+mixin混入类
    path("students7/",views.StudentMixinGenericViewSet.as_view({
        'get': 'list',  #视图类方法，可以是原来的http请求动作，也可以是自定义的方法名
        'post': 'create',
    })),
    re_path("^students7/(?P<pk>\d+)/$",views.StudentMixinGenericViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy',
    })),
    #ReadOnlyModelViewSet
    path("students8/",views.StudentReadOnlyMixinGenericViewSet.as_view({
        'get': 'list',  #视图类方法，可以是原来的http请求动作，也可以是自定义的方法名
        'post': 'create',
    })),
    re_path("^students8/(?P<pk>\d+)/$",views.StudentReadOnlyMixinGenericViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy',
    })),
    # ModelViewSet 最精简 万能视图集
    path("students9/",views.StudentModelViewSet.as_view({
        'get': 'list',  #视图类方法，可以是原来的http请求动作，也可以是自定义的方法名
        'post': 'create',
    })),
    re_path("^students9/(?P<pk>\d+)/$",views.StudentModelViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy',
    })),
]

# 上述视图集路由太复杂，下面使用路由集自动生成路由信息，必须和视图集一起使用
from rest_framework.routers import SimpleRouter, DefaultRouter

# 1.实例化路由类
router =DefaultRouter()  #DefaultRouter比SimpleRouter多个api-root
# 2.给路由去注册视图集
router.register("students10",views.StudentAutoModelViewSet,basename="student10")  #不能用正则,只能生成5个api接口，第一个students10为路由前缀
print('名为demo的app里urls.py打印的自动生成的路由列表:',router.urls)
print(timezone.now())
# 3.把生成的路由列表和urlpatterns进行拼接
urlpatterns+=router.urls