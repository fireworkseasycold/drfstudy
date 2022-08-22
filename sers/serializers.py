# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/7/30 9:55
# @Author : firworkseasycold
# @Email : 1476094297@qq.com
# @File : serializers.py
# @Software: PyCharm
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from stu_api.models import Student

"""
serializers是大润发提供给开发者调用的序列化器模块
里面申明了所有的可用序列化器的基类
Serializer 序列化基类，drf所有序列化器类都必须继承
ModelSerializer 模型序列化器，是序列化器基类的子类，在工作中是除了Serializer外最常用的序列化器基类
"""


class StudentSerializer1(serializers.Serializer):
    """学生信息序列化器"""
    # 1.转化的字段申明
    # 客户端字段=serializers.字段类型(选项=选项值,)
    id = serializers.IntegerField()
    name = serializers.CharField()
    sex = serializers.BooleanField()
    age = serializers.IntegerField()
    description = serializers.CharField()

    # 2.如果序列化器是继承的ModelSerializer，则需要申明调用的模型信息
    # class Meta:
    #     model=模型
    #     fields=["字段1"...]

    # 3.验证数据的对象方法
    # def validate(self,attrs): #validate是固定的
    #     pass
    #     return attrs
    # def validate_<字段名>(self,data): #方法名的格式必须以validate_<字段名>为名称，否则序列化器不识别！
    #   pass
    #   return data

    # 4.模型操作的方法
    # def create(self, validated_data):  #添加数据操作，添加数据后，就自动实现了从字典变成模型对象的过程（反序列化）
    #     pass

    # def update(self, instance, validated_data):  #更新数据操作，更新数据后，就自动实现了从字典变成模型对象的过程
    #     pass

#3.3 验证数据的对象方法3，不常用
def check_classmate(data):
    """外部验证函数"""
    if len(data) !=3:
        raise serializers.ValidationError(detail="班级编号格式不正确，必须是3位！",code="check_classmate")
    #验证完成后务必返回结果，否则最终的验证结果没有该数据
    return data

class StudentSerializer2(serializers.Serializer):
    """学生信息序列化器"""
    # 1.转化的字段申明
    # 客户端字段=serializers.字段类型(选项=选项值,)
    id = serializers.IntegerField(read_only=True)  # read_only=True，在客户端提交数据(反序列化阶段不会要求id字段)
    name = serializers.CharField(required=True)  # required=True， 反序列化阶段必填
    sex = serializers.BooleanField(default=True)  # default=True,序列化阶段，客户端没有提交，则默认为True
    age = serializers.IntegerField(max_value=100, min_value=0,
                                   error_messages={"min_value": "age must be >=0",
                                                   "max_value": "age must be <=100"})  # age在反序列化必须是0<=age<=100
    # validators 外部验证函数选项，列表得到成员函数名，不能是字符串
    classmate = serializers.CharField(validators=[check_classmate])
    description = serializers.CharField(allow_null=True, allow_blank=True)  # 允许客户端不填写内容，或者值为""

    # 2.如果序列化器是继承的ModelSerializer，则需要申明调用的模型信息
    # class Meta:
    #     model=模型
    #     fields=["字段1"...]

    # 3.验证数据的对象方法 3.1 3.2 3.3
    #3.1 def validate(self,attrs): #validate是固定的
    #     pass
    #     return attrs
    def validate(self,attrs):
        """验证来自客户端的所有数据
        类似会员注册的密码和确认密码，就只能在validate方法中校验
        validate是固定方法名，
        参数：attrs,是在序列化器实例化时的data选项数据"""
        # print(f"attrs={attrs}")
        #举例：：301班只能有女生，不能有男生
        # if attrs["classmate"]=="301" and attrs["sex"]:
        if attrs.get("classmate")=="301" and attrs.get("sex"):
            raise serializers.ValidationError(detail="301只能有女生",code="validate")
        return attrs

    #3.2 def validate_<字段名>(self,data): #方法名的格式必须以validate_<字段名>为名称，否则序列化器不识别！
    #   pass
    #   return data
    def validate_name(self,data):
        """验证单个字段
        方法名的格式必须以validate_<字段名>为名称，否则序列化器不识别！
        validate开头的方法，会自动被is_valid调用
        """
        # print(f"name={data}")
        #举例：
        if data in ["python","django"]:
            #在序列化器中，验证失败可以通过抛出异常的方式来告知is_valid
            raise serializers.ValidationError(detail="学生姓名不能是python或django",code="validate_name")
        #验证成功后，必须返回数据，否则最终的验证集中，不会出现这个数据了
        return data


    # 4.模型操作的方法
    # def create(self, validated_data):  #添加数据操作，添加数据后，就自动实现了从字典变成模型对象的过程（反序列化）
    #     pass
    def create(self, validated_data):
        """添加数据"""
        #添加数据操作，方法名固定为create，固定参数validated_data就是验证成功以后的结果
        student = Student.objects.create(**validated_data)
        return student

    # def update(self, instance, validated_data):  #更新数据操作，更新数据后，就自动实现了从字典变成模型对象的过程
    #     pass
    def update(self, instance, validated_data):
        """
        更新数据操作
        方法名固定为update，
        固定参数instance,实例化序列化器对象时，必须传入的模型对象
        固定参数validated_data就是验证成功以后的结果
        """
        # instance.name=validated_data["name"]
        # instance.sex=validated_data["sex"]
        # instance.age=validated_data["age"]
        # instance.classmate=validated_data["classmate"]
        # instance.description=validated_data["description"]
        for key,value in validated_data.items():
            setattr(instance,key,value)
        instance.save() #调用模型对象的save方法，和视图中serializer.save()不是用同一个类的方法
        return instance

#以上代码太多，大多数代码就没有必要写，实际用ModelSerializer，如下

class StudentModelSerializer(serializers.ModelSerializer):
    # 1.转化的字段申明
    # 字段名=serializers.字段类型(选项=选项值, )
    nickname = serializers.CharField(default="佚名",read_only=True,allow_null=True,allow_blank=True)  # 自定义数据模型里没有的字段,没有default且view中未赋值则不显示
    # 2.如果序列化器是继承的ModelSerializer，则需要申明调用的模型信息
    #必须给meta两个属性
    # class Meta:
    #     model=模型名 #必填
    #     fields=["字段1"...] #必填,可以是字符串和列表/元组,"__all__"表示所有字段
    #     exclude = [...]  # 表示排除字段，与fields互斥，用一个就行
    #     read_only_fields=[] #选填只读字段，表示设置这里的字段只会在序列化阶段使用
    #     extra_kwards={ # 选填，字段额外选项申明
    #         "字段名":{
    #             "选项"："选项值"
    #         }
    #     }
    class Meta:
        model=Student
        fields=["id","name","age","sex","nickname"]
        read_only_fields=["id"]
        extra_kwargs = {
            "age": {
                "min_value": 5,
                "max_value": 20,
                "error_messages": {
                    "min_value": "年龄的最小值必须大于等于5",
                    "max_value": "年龄的最大值必须小于等于20",
                },
            },
        }
    # 3.验证数据的对象方法
    #有需要的时候重写
    #例如密码加密
    # def create(self,validated_data):
    #     validated_data["password"]=make_password(validated_data["password"])
    #     super().create(validated_data)
    # 4.模型操作的方法
