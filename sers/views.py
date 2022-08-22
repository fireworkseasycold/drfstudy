import json

from django.http import JsonResponse
from django.views import View
from .serializers import StudentSerializer1, StudentSerializer2, StudentModelSerializer  #自动导包快捷键alt+enter
from stu_api.models import Student

# Create your views here.
#这里用django的视图类，不会有drf界面
class StudentView1(View):
    """序列化器-序列化调用-一个或多个"""
    def get1(self,request):
        """序列化器-序列化调用-序列化一个模型对象"""
        #1.获取数据集
        student=Student.objects.first()
        # 2.实例化序列化器，得到序列化对象，需要传输数据
        serializer=StudentSerializer1(instance=student)
        # 3.调用序列化对象的data属性方获取转换后的数据
        data = serializer.data
        # 4.响应数据
        return JsonResponse(data=data, status=200, safe=False, json_dumps_params={'ensure_ascii': False})

    def get2(self,request):
        """序列化器-序列化阶段的调用-序列化多个模型对象"""
        #1.获取数据集
        student_list=Student.objects.all()
        #2.实例化序列化器，得到序列化对象[传递到序列化器的模型对象如果是多个，务必使用many=True,否则报错'QuerySet' object has no attribute 'id'.
        serializer=StudentSerializer1(instance=student_list,many=True) #many=True表示多个模型对象
        #3.调用序列化对象的data属性方获取转换后的数据
        data=serializer.data
        #4.响应数据
        return JsonResponse(data=data,status=200,safe=False,json_dumps_params={'ensure_ascii':False}) #使用safe=False处理In order to allow non-dict objects to be serialized set the safe parameter to False.

    def get3(self,request):
        """反序列化，采用字段选项来验证数据[验证失败不抛出异常]，例如给个age=150"""
        #1.接收客户端提交的数据
        # data=json.dumps(request.body)
        #模拟来自客户端的数据
        data={
            "name":"小红",
            "age":117,
            "classmate":"301",
            "description":"这家伙很懒，申明都没留下~"
        }
        #1.1 实例化序列器，获取序列化对象
        serializer=StudentSerializer2(data=data)
        #1.2 调用序列化器进行验证数据
        ret = serializer.is_valid() #不抛出异常

        print(f"ret={ret}")
        #1.3 获取验证以后的结果
        if ret:
            # print(serializer.validated_data)
            return JsonResponse(dict(serializer.validated_data))
        else:
            # print(serializer.errors)
            return JsonResponse(serializer.errors)
        #2.操作数据库
        #3.返回结果

    def get4(self, request):
            """反序列化，采用字段选项来验证数据[验收失败抛出异常，工作中最常用]"""
            # 1.接收客户端提交的数据
            # data=json.dumps(request.body)
            # 模拟来自客户端的数据
            data = {
                "name": "小红",
                "age": 11,
                "classmate": "3077",
                "description": "这家伙很懒，申明都没留下~"
            }
            # 1.1 实例化序列器，获取序列化对象
            serializer = StudentSerializer2(data=data)
            # 1.2 调用序列化器进行验证数据
            serializer.is_valid(raise_exception=True)  # 抛出异常，代码不会往下执行
            # 1.3 获取验证以后的结果
            # print(serializer.validated_data)
            # 2.操作数据库
            # 3.返回结果
            return JsonResponse(dict(serializer.validated_data))

    def get5(self, request):
            """反序列化，验证完成后添加数据入库"""
            # 1.接收客户端提交的数据
            # data=json.dumps(request.body)
            # 模拟来自客户端的数据
            data = {
                "name": "小红",
                "age": 11,
                "sex":False,
                "classmate": "301",
                "description": "这家伙很懒，申明都没留下~"
            }
            # 1.1 实例化序列器，获取序列化对象
            serializer = StudentSerializer2(data=data)
            # 1.2 调用序列化器进行验证数据
            serializer.is_valid(raise_exception=True)  # 抛出异常，代码不会往下执行

            # # 1.3 获取验证以后的结果
            # data=serializer.validated_data
            # # 2.操作数据库
            # student=Student.objects.create(**data)
            # serializer = StudentSerializer2(instance=student)
            # 注释掉的这几句，可以移植到serializers里的create：student = Student.objects.create(**serializer.validated_data)，并在view中serializer.save()，工作中的用法

            # 2.获取验证以后的结果，操作数据库
            # print(serializer.data)
            serializer.save() #会根据实例化序列器的时候，根据传入的instance属性，没有传入instance自动调用create，或者有传入instance自动调用update方法；没有这句会发现结果少个id


            # 3.返回结果
            return JsonResponse(serializer.data,status=201)

    def get(self, request):
            """反序列化，验证完成后，更新数据入库"""
            #1.根据客户端访问的url地址中，获取pk值
            #sers/students/2/ path("/students/(?<pk>)d+/",views.StudentView.as_view(),
            pk=6
            try:
                student=Student.objects.get(pk=pk)
            except Student.DoesNotExist:
                return JsonResponse({"errors":"当前学生不存在"},status=400)

            # 2.接收客户端提交的修改数据
            # data=json.dumps(request.body)
            # 模拟来自客户端的数据
            # data = {
            #     "name": "xiaohong",
            #     "age": 18,
            #     "sex": False,
            #     "classmate": "303",
            #     "description": "这家伙很懒，申明都没留下~"
            # }
            # 3.修改操作中的实例化序列化器对象
            # serializer=StudentSerializer2(instance=student,data=data)
            #附加：默认序列化器必须传递所有required的字段，否则会抛出异常，但是我们可以使用partial参数来允许部分字段更新
            #举例：更新name，不需要验证其他的字段，可以设置partial=True
            serializer=StudentSerializer2(instance=student,data={"name":'xiaomi'},partial=True)
            # 4.验证数据
            serializer.is_valid(raise_exception=True)
            #5.入库
            #request.user#是django中记录当前登录用户的模型对象
            serializer.save(owner=request) #附加：可以在save中，传递一些不需要验证的数据到模型里面
            #6.返回结果
            return JsonResponse(serializer.data,status=201)


class StudentView(View):
    """模型序列化器"""
    def get1(self,request):
        """序列化器-序列化调用-序列化一个模型对象"""
        #1.获取数据集
        student=Student.objects.first()
        student.nickname="小学生" #临时加进去的模型没有的字段，需要serializers中自定义
        # 2.实例化序列化器，得到序列化对象，需要传输数据
        serializer=StudentModelSerializer(instance=student)
        # 3.调用序列化对象的data属性方获取转换后的数据
        data = serializer.data
        # 4.响应数据
        return JsonResponse(data=data, status=200, safe=False, json_dumps_params={'ensure_ascii': False})

    def get2(self,request):
        """序列化器-序列化阶段的调用-序列化多个模型对象"""
        #1.获取数据集
        student_list=Student.objects.all()
        #2.实例化序列化器，得到序列化对象[传递到序列化器的模型对象如果是多个，务必使用many=True,否则报错'QuerySet' object has no attribute 'id'.
        serializer=StudentModelSerializer(instance=student_list,many=True) #many=True表示多个模型对象
        #3.调用序列化对象的data属性方获取转换后的数据
        data=serializer.data
        #4.响应数据
        return JsonResponse(data=data,status=200,safe=False,json_dumps_params={'ensure_ascii':False}) #使用safe=False处理In order to allow non-dict objects to be serialized set the safe parameter to False.

    def get3(self,request):
        """反序列化，采用字段选项来验证数据[验证失败不抛出异常]，例如给个age=150"""
        #1.接收客户端提交的数据
        # data=json.dumps(request.body)
        #模拟来自客户端的数据
        data={
            "name":"小红",
            "age":117,
            "classmate":"301",
            "description":"这家伙很懒，申明都没留下~"
        }
        #1.1 实例化序列器，获取序列化对象
        serializer=StudentModelSerializer(data=data)
        #1.2 调用序列化器进行验证数据
        ret = serializer.is_valid() #不抛出异常
        # print(f"ret={ret}")
        #1.3 获取验证以后的结果
        if ret:
            # print(serializer.validated_data)
            return JsonResponse(dict(serializer.validated_data))
        else:
            # print(serializer.errors)
            return JsonResponse(serializer.errors)
        #2.操作数据库
        #3.返回结果

    def get4(self, request):
            """反序列化，采用字段选项来验证数据[验收失败抛出异常，工作中最常用]"""
            # 1.接收客户端提交的数据
            # data=json.dumps(request.body)
            # 模拟来自客户端的数据
            data = {
                "name": "小红",
                "age": 11,
                "classmate": "3077",
                "description": "这家伙很懒，申明都没留下~"
            }
            # 1.1 实例化序列器，获取序列化对象
            serializer = StudentModelSerializer(data=data)
            # 1.2 调用序列化器进行验证数据
            serializer.is_valid(raise_exception=True)  # 抛出异常，代码不会往下执行
            # 1.3 获取验证以后的结果
            # print(serializer.validated_data)
            # 2.操作数据库
            # 3.返回结果
            return JsonResponse(dict(serializer.validated_data))

    def get5(self, request):
            """反序列化，验证完成后添加数据入库"""
            # 1.接收客户端提交的数据
            # data=json.dumps(request.body)
            # 模拟来自客户端的数据
            data = {
                "name": "小H",
                "age": 11,
                "sex":False,
                "classmate": "301",
                "description": "这家伙很懒，申明都没留下~"
            }
            # 1.1 实例化序列器，获取序列化对象
            serializer = StudentModelSerializer(data=data)
            # 1.2 调用序列化器进行验证数据
            serializer.is_valid(raise_exception=True)  # 抛出异常，代码不会往下执行

            # # 1.3 获取验证以后的结果
            # data=serializer.validated_data
            # # 2.操作数据库
            # student=Student.objects.create(**data)
            # serializer = StudentSerializer2(instance=student)
            # 注释掉的这几句，可以移植到serializers里的create：student = Student.objects.create(**serializer.validated_data)，并在view中serializer.save()，工作中的用法

            # 2.获取验证以后的结果，操作数据库
            # print(serializer.data)
            serializer.save() #会根据实例化序列器的时候，根据传入的instance属性，没有传入instance自动调用create，或者有传入instance自动调用update方法；没有这句会发现结果少个id


            # 3.返回结果
            return JsonResponse(serializer.data,status=201)

    def get(self, request):
            """反序列化，验证完成后，更新数据入库"""
            #1.根据客户端访问的url地址中，获取pk值
            #sers/students/2/ path("/students/(?<pk>)d+/",views.StudentView.as_view(),
            pk=6
            try:
                student=Student.objects.get(pk=pk)
            except Student.DoesNotExist:
                return JsonResponse({"errors":"当前学生不存在"},status=400)

            # 2.接收客户端提交的修改数据
            # data=json.dumps(request.body)
            # 模拟来自客户端的数据
            data = {
                "name": "xiaohei",
            }
            # 3.修改操作中的实例化序列化器对象
            #附加：默认序列化器必须传递所有required的字段，否则会抛出异常，但是我们可以使用partial参数来允许部分字段更新
            #举例：更新name，不需要验证其他的字段，可以设置partial=True
            serializer=StudentModelSerializer(instance=student,data=data,partial=True)
            # 4.验证数据
            serializer.is_valid(raise_exception=True)
            #5.入库
            #request.user#是django中记录当前登录用户的模型对象
            serializer.save(owner=request) #附加：可以在save中，传递一些不需要验证的数据到模型里面
            #6.返回结果
            return JsonResponse(serializer.data,status=201)
