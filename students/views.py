from rest_framework.viewsets import ModelViewSet
from stu_api.models import Student
from .serializers import StudentExampleModelSerializer


# Create your views here.
#使用drf视图类
class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentExampleModelSerializer
