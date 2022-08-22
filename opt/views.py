from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication,BasicAuthentication

from django.contrib.auth.middleware import AuthenticationMiddleware
from school.models import Student
from school.serializers import StudentschoolModelSerializer
from drf.authentication import ExampleAuthentication #自定义认证
from drf.permissions import ExamplePermission #自定义权限
# Create your views here.



class ExampleView(APIView):
    # 类属性
    #认证
    authentication_classes=[ExampleAuthentication,] #可以在settings里配置改为全局认证，然后这里使用自定义的覆盖全局给局部用
    #自定义的ExampleAuthentication是http://127.0.0.1:8000/opt/example/?user=root&pwd=xl123456


    def get(self,request):
        """单独设置认证方式"""
        #失败会401未认证/403权限被禁止
        print(request.user) #是在中间件AuthenticationMiddleware中完成识别，如果没有登录则为AnonymousUser表示匿名
        # print(type(request.user))
        if request.user.id is None:  #不建议这么写，可能会抛出AttributeError: 'NoneType' object has no attribute 'id'
            return Response("未登录用户：游客")
        else:
            return Response({"已登录用户":"{request.user}"})

    def post(self,request):
        return Response({"msg":"ok"})

    """
    注意:使用限流后， 这里是内置认证以后的频率校验, 如果使用的自定义的认证, request.user是没有is_authenticated属性的
    抛出异常: 'xxx' object has no attribute 'is_authenticated'
    """



class ExampleView2(RetrieveAPIView):

    # 权限
    # permission_classes = [IsAuthenticated] #权限 只有登录用户才可访问
    # permission_classes = [IsAdminUser] #权限 只有管理员才可访问，user.is_staff为rue
    # permission_classes = [IsAuthenticatedOrReadOnly] #权限 游客只读，已经登陆的用户则可以对数据进行任意操作

    # 自定义的权限
    permission_classes = [ExamplePermission]


    queryset = Student.objects.all()
    serializer_class=StudentschoolModelSerializer
#     http://127.0.0.1:8000/opt/permission/2?user=root  user!=root则提示无权限

    #限流局部配置 需要配合全局配置中DEFAULT_THROTTLE_CLASSES来设置频率，注释掉settings里的
    # throttle_classes = [UserRateThrottle]
    #自定义限流
    # throttle_classes = "vip"  #在settings里的自定义限流属性
    throttle_classes = "vvip"  #在settings里的自定义限流属性

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
class ExampleView3(ListCreateAPIView,RetrieveUpdateDestroyAPIView):
    """过滤与排序"""
    # http://127.0.0.1:8000/opt/filter/?age>18&sex=1
    #http://127.0.0.1:8000/opt/filter/?ordering=age
    queryset=Student.objects.all()
    serializer_class=StudentschoolModelSerializer
    # filter_backends = [DjangoFilterBackend] #drf过滤局部配置
    # filter_fields=["sex","age"]

    filter_backends = [OrderingFilter]  # drf排序局部配置
    ordering_fields=['id','age']


from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import  LimitOffsetPagination,PageNumberPagination

class StudentPageNumberPagination(PageNumberPagination):
    """自定义分页器"""
    page_query_param = "page" #查询字符串中代表页码的变量名
    page_size_query_param = "size" #查询字符串中代表每一页数据的变量名
    page_size = 2 #每一页数据量
    max_page_size = 4 #允许客户端通过查询字符串调整的最大单页数据量 #用于多个查询字符串

class ExampleView4(ListCreateAPIView):
    # http://127.0.0.1:8000/opt/pagination/?page=1"
    queryset = Student.objects.all()
    serializer_class = StudentschoolModelSerializer

    #本视图关闭来自全局的分页
    # pagination_class =None

    # #局部分页
    # pagination_class = PageNumberPagination
    pagination_class = StudentPageNumberPagination

class ExampleView5(APIView):
    """使用自定义异常"""
    def get(self,request):
        try :
            1/0
        except:
            return Response({"msg":'0不能作为除数'})
        return Response({"msg":'ok'})
