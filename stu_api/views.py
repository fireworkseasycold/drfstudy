import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Student

# Create your views here.


"""
POST /students/   添加一个学生信息
GET /students/   获取所有学生信息

GET /students/<pk>  获取一个学生信息
PUT /students/<pk>  更新一个学生信息
DELETE /students/<pk>  删除一个学生信息

一个路由对应一个视图类，所以可以把5个api分成两个类来完成

"""


class StudentView(View):
    """学生视图"""

    def post(self, request):
        """添加一个学生信息"""
        # 1.接收客户端提交的数据
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        classmate = request.POST.get('classmate')
        description = request.POST.get('description')
        # 2.操作数据库，保存数据
        instance = Student.objects.create(
            name=name,
            sex=sex,
            age=age,
            classmate=classmate,
            description=description,
        )
        # 3.返回结果，访问405,需要postman，输入表单
        return JsonResponse(data={"id": instance.pk, "name": instance.name, "sex": instance.sex, "age": instance.age,
                                  "classmate": instance.classmate, "description": instance.description, }, status=201)

    def get(self, request):
        """获取多个学生信息"""
        # 1.读取数据库
        students_list = list(Student.objects.values())
        # print(students_list)
        # 2.返回数据
        return JsonResponse(data=students_list, status=200,
                            safe=False)  # In order to allow non-dict objects to be serialized set the safe parameter to False. 解决：safe=False,或者data是dict


class StudentInfoView(View):
    def get(self, request, pk):
        """获取一条数据"""
        try:
            instance = Student.objects.get(pk=pk)
            return JsonResponse(
                data={"id": instance.pk, "name": instance.name, "sex": instance.sex, "age": instance.age,
                      "classmate": instance.classmate, "description": instance.description, }, status=200)
        except Student.DoesNotExist:
            return JsonResponse(data={}, status=404)  # 没有内容

    def put(self, request, pk):
        """更新一个学生信息"""
        # """
        # #错误写法   #put不支持表单提交
        # name = request.POST.get('name')
        # print(f"name={request.body}")  #使用格式化字符串打印
        # sex = request.POST.get('sex')
        # age = request.POST.get('age')
        # classmate = request.POST.get('classmate')
        # description = request.POST.get('description')
        # """
        # 1.接收数据
        data = json.loads(request.body)  # 前端使用ajax发送json数据
        # print(f"data={data}")
        # alt+鼠标左键垂直,或者alt+j
        name = data.get('name')
        sex = data.get('sex')
        age = data.get('age')
        classmate = data.get('classmate')
        description = data.get('description')
        # 2.操作数据库，保存数据
        try:
            instance = Student.objects.get(pk=pk)
            instance.name = name
            instance.sex = sex
            instance.age = age
            instance.classmate = classmate
            instance.description = description
            instance.save()
        except Student.DoesNotExist:
            return JsonResponse(data={}, status=404)  # 没有内容
        # 3.返回结果，访问405,需要postman，输入表单
        return JsonResponse(data={
            "id": instance.pk,
            "name": instance.name,
            "sex": instance.sex,
            "age": instance.age,
            "classmate": instance.classmate,
            "description": instance.description,
        }, status=201)

    def delete(self, request, pk):
        """删除一个学生信息"""
        try:
            Student.objects.filter(pk=pk).delete()
        except:
            pass
        return JsonResponse(data={}, status=204)
