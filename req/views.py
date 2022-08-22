from django.views import View
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response  #drf的response是django的子类
from rest_framework import status #保存了所有HTTP响应状态对应的常量

# Create your views here.
class StudentView(View):
    def get(self,request):  #django提供的View视图
        print(f"request={request}") #request=<WSGIRequest: GET '/req/students1/'>

        return HttpResponse("ok")


class StudentAPIView(APIView):
    # drf request:
    # data request.data 返回解析之后的请求体数据
    # query_params  request.query_params 与django request.GET等同
    # request._request #获取django封装的request对象
    # drf data status_code response 工作中少用，一般是做缓存
    def get(self,request):
        # 获取请求体数据
        print(f"drf.request={request}") #request=<rest_framework.request.Request: GET '/req/students/'>
        print(f"django.request={request._request}") #django.request=<WSGIRequest: GET '/req/students/'>
        return Response({"msg":"ok"},status=status.HTTP_202_ACCEPTED,headers={"myResponseHeaders":"drfstudy"}) #headers新的自定义可以在drfapi界面看到
        # Response(data,status,template_name,headers,exception,content_type)

    def post(self,request):
        #添加数据
        """ 获取请求体数据"""
        print(f"request.data={request.data}") #接收的数据已经被Parse解析器转换成字典数据
        # 使用postman body模拟提交
        #客户端提交json数据
        # request.data = {'name': 'xiaoliz', 'password': 123456}
        #客户端提交表单数据
        # request.data = < QueryDict: {'name': ['xiaoliz'], 'password': ['123456'], 'sex': ['1']} >
        print(request.data.get("name"))

        """获取查询参数又叫查询字符串""" #?key1=value1&...
        print(f"request.query_params={request.query_params}")

        return Response({"msg": "ok"})

    def put(self,request):
        return Response({"msg": "ok"})

    def patch(self,request):
        # 获取请求体数据
        return Response({"msg": "ok"})

    def delete(self,request):
        return Response({"msg": "ok"})
