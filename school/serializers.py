# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/8/17 8:55
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : serializer.py
# @Software: PyCharm
from rest_framework import serializers

from school.models import Teacher,Student,Achievement,Course

class CourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'

class AchievementModelSerializer(serializers.ModelSerializer):
    #序列化器嵌套的写法1，单独嵌套一个，重写模型对应外键，默认为外键id,所以需要再次序列化来拿数据，可选many=True参数来实现序列化嵌套多个
    # course=CourseModelSerializer() #course为本表的外键字段，本表为从表 太麻烦
    #序列化器嵌套的写法2 source指定数据
    cj=serializers.CharField(default='课程') #写死了
    course_name=serializers.CharField(source="course.name") #写为外键字段course对应对象的字段name
    teacher_name=serializers.CharField(source="course.teacher.name")
    class Meta:
        model=Achievement
        fields=['id','course','score','create_dtime','cj','course_name','teacher_name']

class AchievementModelSerializer2(serializers.ModelSerializer):
    class Meta:
        model=Achievement
        #从成绩模型-课程=1
        #从成绩模型-课程-成绩=2
        #从老师模型-课程-成绩-学生=3
        fields="__all__"
        # 序列化器嵌套的写法3 深度属性，1代表序列化器层数
        # depth=1
        depth=2 #这里从成绩开始，所以只有两层
        #序列化器嵌套写法4 在模型里自定义方法，例如def achievement()

class StudentschoolModelSerializer(serializers.ModelSerializer):
    # s_achievement=AchievementModelSerializer(many=True) #对应写法1默认情况下，模型经过序列化器的数据转换，对于外键的信息，仅仅是把数据库李外键的id返回,所所以这里再次经过序列化器进行转换,才能显示数据;这里就叫做序列化器的嵌套，注意这里不能是非外键字段，必须是外键
    # # 注意AttributeError: Got AttributeError when attempting to get a value for field `create_dtime` on serializer `AchievementModelSerializer`.The serializer field might be named incorrectly and not match any attribute or key on the `RelatedManager` instance.Original exception text was: 'RelatedManager' object has no attribute 'create_dtime'.这是因为没有带(many=True),因为这里是关系是多个数据

    # s_achievement=AchievementModelSerializer2(many=True) #对应写法3
    class Meta:
        model=Student
        # fields=['id','name','sex','s_achievement','achievement']  #s_achievement为从表的课程外键字段，本表为主表;
        fields=['id','name','sex','achievement']  # 'achievement'为model自定义方法,对应序列化器的写法4


class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields='__all__'

