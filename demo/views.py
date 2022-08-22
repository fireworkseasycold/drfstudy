from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet,GenericViewSet,ReadOnlyModelViewSet,ModelViewSet

from stu_api.models import Student
from .serializers import StudentModelSerializer, Student2ModelSerializer

# Create your views here.
#普通视图 2个视图基类，5个拓展类，GenericAPIView（通用视图类）的9个视图子类
#视图集ViewSet

"""
POST /students/   添加一个学生信息
GET /students/   获取所有学生信息

GET /students/<pk>  获取一个学生信息
PUT /students/<pk>  更新一个学生信息
DELETE /students/<pk>  删除一个学生信息

一个路由对应一个视图类，所以可以把5个api分成两个类来完成

"""

#APIview基本视图类
class StudentAPIView(APIView):
    def get(self,request):
        """获取所有学生信息"""
        # 1.从数据库中读取学生列表信息
        student_list=Student.objects.all()
        # print(student_list)
        # 2.实例化序列器，获取序列化对象
        serializer=StudentModelSerializer(instance=student_list,many=True)
        # print(serializer.data)
        # 3.转换数据并返回给客户端
        return Response(serializer.data)

    def post(self,request):
        #1.获取客户端提交的数据，实例化序列化器获取序列化对象
        serializer=StudentModelSerializer(data=request.data)
        #2.反序列化【验证，保存数据】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #3.返回新增模型数据给客户端
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class StudentInfoAPI(APIView):
    def get(self,request,pk):
        """获取一条数据"""
        #1.使用pk作为条件获取模型对象
        try:
            student=Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #2.序列化
        serializer=StudentModelSerializer(instance=student)
        #3.返回结果
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk):
        """单更新数据"""
        # 1.使用pk作为条件获取模型对象
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2.获取客户端提交的数据
        serializer = StudentModelSerializer(instance=student,data=request.data,partial=False) #参数partial=True，就变成单局部修改
        # 3.反序列化【验证，保存数据】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4.返回结果
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def patch(self): """单/批量局部改"""

    def delete(self,request,pk):
        """删除数据"""
        # 1.使用pk作为条件获取模型对象
        try:
            Student.objects.get(pk=pk).delete()
        except Student.DoesNotExist:
            pass
        #2.返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)


#以上代码可重用，所以下面优化使用GenericAPIView（通用视图类）

class StudentGenericAPIView(GenericAPIView):
    #只有一个查询集
    queryset = Student.objects.all()
    #如果有多个查询集
    # def get_queryset(self):  #GenericAPIView源码方法重写
    #     queryset=self.request.queryset
    #     return queryset.accounts.all()
    # 如果整个视图只有使用一个序列化器
    serializer_class = StudentModelSerializer
    #整个视图类有多个序列化器
    # def get_serializer_class(self): #内置方法
    #     # 例如
    #     if self.request.method.lower()=='put':
    #         return StudentModelSerializer
    #     else:
    #         return Student2ModelSerializer
    def get(self,request):
        """获取所有学生信息"""
        #1.从数据库中读取模型列表信息 #根据面向对象，调用方法而不是属性
        queryset=self.get_queryset() #GenericAPIView提供的get_queryset
        #2.序列化
        serializer=self.get_serializer(instance=queryset,many=True)  #少了many会没有循环，报错'QuerySet' object has no attribute 'name'.
        #3.返回数据并返回给客户端
        return Response(serializer.data)
    def post(self,request):
        """添加一个数据"""
        # 1.获取客户端提交的数据，实例化序列化器获取序列化对象
        serializer = self.get_serializer(data=request.data)
        # 2.反序列化【验证，保存数据】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3.返回新增模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StudentInfoGenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self,request,pk):
        #1.使用pk作为条件获取模型对象
        instance=self.get_object()
        #instance=self.queryset().get(pk=student.id)
        #2.序列化
        serializer=self.get_serializer(instance=instance)
        #3.返回结果
        return Response(serializer.data)

    def put(self,request,pk):
        # 1.使用pk作为条件获取模型对象
        instance = self.get_object()
        #2.获取客户端提交的数据
        serializer = self.get_serializer(instance=instance,data=request.data)
        # 3.反序列化
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3.返回结果
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def delete(self,request,pk):
        #1.根据pk值获取要删除的数据并删除
        self.get_object().delete()
        #2.返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)


"""使用drf内置的模型扩展类[混入类]结合GenericAPIView实现通用视图方法的简写操作,5个
from rest_framework.mixins import ListModelMixin  获取多条数据，返回响应结果 list
from rest_framework.mixins import CreateModelMixin 添加一条数据，返回响应结果 create
from rest_framework.mixins import RetrieveModelMixin 获取一条数据，返回响应结果 retrieve
from rest_framework.mixins import UpdateModelMixin 更新一条数据，返回响应结果 update
from rest_framework.mixins import DestroyModelMixin 删除一条数据，返回响应结果 destory
"""
class StudentMixinView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    def get(self,request):
        """获取所有数据"""
        return self.list(request)
    def post(self,request):
        """添加一条数据"""
        return self.create(request)

class StudentInfoMixinView(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    def get(self,request,pk):
        #获取一条数据
        return self.retrieve(request,pk=pk)
    def put(self,request,pk):
        """更新一条数据"""
        return self.update(request,pk=pk)
    def delete(self,request,pk):
        """删除一条数据"""
        return self.destroy(request,pk=pk)

"""
比上方更加精简的视图子类
视图子类是通用视图类和模型拓展类的子类

ListAPIView = GenericAPIView + ListModelMixin  获取多条数据
CreateAPIView = GenericAPIView + CreateModelMixin 添加一条数据
RetrieveAPIView= GenericAPIView +RetrieveModelMixin 获取一条数据
UpdateAPIView = GenericAPIView + UpdateModelMixin 更新一条数据
DestroyAPIView = GenericAPIView + DestroyModelMixin 删除一条数据
组合视图子类
ListCreateAPIView
RetrieveUpdateAPIView
RetrieveDestroyAPIView
RetrieveUpdateDestroyAPIView
"""


class StudentView(ListAPIView,CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    #除非在get之前需要进行自己的操作，否则不用写get，因为源码有了


class StudentInfoView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

"""
上面的接口在实现过程中，也存在代码重复的情况，我们如果合并成一个接口，则需要考虑两个问题：
1.路由的合并问题
2.get方法重复问题
drf提供了基本视图集可以解决上面的问题
ViewSet  基本视图集
GenericViewSet  通用视图集 ，同时让代码更加通用
"""
class StudentViewSet(ViewSet):
    def get_list(self,request):
        """获取所有学生信息"""
        # 1.从数据库中读取学生列表信息
        student_list = Student.objects.all()
        # print(student_list)
        # 2.实例化序列器，获取序列化对象
        serializer = StudentModelSerializer(instance=student_list, many=True)
        # print(serializer.data)
        # print(self.get)  #<bound method StudentViewSet.get_list of <demo.views.StudentViewSet object at 0x000001D51109D9E8>>
        print(id(self.get),id(self.get_list))  #3210277396040 3210277177928

        # 3.转换数据并返回给客户端
        return Response(serializer.data)

    def post(self, request):
        # 1.获取客户端提交的数据，实例化序列化器获取序列化对象
        serializer = StudentModelSerializer(data=request.data)
        # 2.反序列化【验证，保存数据】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3.返回新增模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_student_info(self,request,pk):
        """获取一条数据"""
        #1.使用pk作为条件获取模型对象
        try:
            student=Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #2.序列化
        serializer=StudentModelSerializer(instance=student)
        #3.返回结果
        return Response(serializer.data,status=status.HTTP_200_OK)

    def update_student_info(self, request, pk):
        """单更新数据"""
        # 1.使用pk作为条件获取模型对象
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2.获取客户端提交的数据
        serializer = StudentModelSerializer(instance=student, data=request.data,
                                            partial=False)  # 参数partial=True，就变成单局部修改
        # 3.反序列化【验证，保存数据】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 4.返回结果
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # def patch(self): """单/批量局部改"""

    def delete_student_info(self, request, pk):
        """删除数据"""
        # 1.使用pk作为条件获取模型对象
        try:
            Student.objects.get(pk=pk).delete()
        except Student.DoesNotExist:
            pass
        # 2.返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)

"""GenericViewSet通用视图集"""

class StudentGenericViewSet(GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    def list(self,request):
        """获取所有学生信息"""
        #1.从数据库中读取模型列表信息 #根据面向对象，调用方法而不是属性
        queryset=self.get_queryset() #GenericAPIView提供的get_queryset
        #2.序列化
        serializer=self.get_serializer(instance=queryset,many=True)  #少了many会没有循环，报错'QuerySet' object has no attribute 'name'.
        #3.返回数据并返回给客户端
        return Response(serializer.data)
    def create(self,request):
        """添加一个数据"""
        # 1.获取客户端提交的数据，实例化序列化器获取序列化对象
        serializer = self.get_serializer(data=request.data)
        # 2.反序列化【验证，保存数据】
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3.返回新增模型数据给客户端
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get_student_info(self,request,pk):
        #1.使用pk作为条件获取模型对象
        instance=self.get_object()
        #instance=self.queryset().get(pk=student.id)
        #2.序列化
        serializer=self.get_serializer(instance=instance)
        #3.返回结果
        return Response(serializer.data)

    def update_student_info(self,request,pk):
        # 1.使用pk作为条件获取模型对象
        instance = self.get_object()
        #2.获取客户端提交的数据
        serializer = self.get_serializer(instance=instance,data=request.data)
        # 3.反序列化
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 3.返回结果
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def delete_student_info(self,request,pk):
        #1.根据pk值获取要删除的数据并删除
        self.get_object().delete()
        #2.返回结果
        return Response(status=status.HTTP_204_NO_CONTENT)



"""GenericViewSet通用视图集+mixin混入类"""

class StudentMixinGenericViewSet(GenericViewSet,ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

"""上面的接口继承的父类太多了
可以继续让一些合并的视图父集让视图继承
ReadOnlyModelViewSet=ListModelMixin+RetrieveModelMixin+GenericViewSet
    获取一条数据
    获取多条数据
ModelViewSet
    实现了5个api接口    
"""

class StudentReadOnlyMixinGenericViewSet(ReadOnlyModelViewSet,CreateModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

"""
ModelViewSet
"""
class StudentModelViewSet(ModelViewSet):  #万能视图集
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


"""搭配视图集使用路由集,路由集只能自动生成5个默认api，其他需要@action"""
class StudentAutoModelViewSet(ModelViewSet):  #万能视图集
    """
    学生信息模型
    :create:添加一个学生信息
    :read: 查询一个学生信息
    """
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    #自定义登录接口-例如login
    @action(methods=["get"],detail=False)  #必须有action声明，否则自定义的动作无法自动生成路由,反而要自己写
    #detail=False,则函数没有pk参数 表示路径： 路由前缀/action方法名/
    #http://127.0.0.1:8000/demo/students10/login1/
    def login1(self,request):
        """登录视图"""
        return Response({"msg":'登录成功'})

    @action(methods=["get"], detail=True)
    #detail=True,函数必须有pk参数 表示路径： 路由前缀/<pk>/action方法名/
    # http://127.0.0.1:8000/demo/students10/10/login2/
    def login2(self,request,pk):
        """登录视图"""
        return Response({"msg":'登录成功'})

    @action(methods=["get"], detail=False,url_path='user/login')
    # url_path:路由后缀 print(router.urls)可以看到
    # http://127.0.0.1:8000/demo/students10/user/login/  #前缀students10  后缀user/login
    def login3(self, request):
        """登录视图"""
        return Response({"msg": '登录成功'})

    @action(methods=["get"], detail=True, url_path='login/log')
    # http://127.0.0.1:8000/demo/students10/10/login/log/  #前缀students10  后缀login/log
    def login_log(self, request,pk):
        """用户登录历史记录"""
        #视图集类比普通的视图类，多一个属性action
        print(self.request.method) #获取客户端的http请求
        print(self.action) #获取客户端请求的视图方法名（ViewSet提供的）login_log
        return Response({"msg": '用户登录历史记录'})

