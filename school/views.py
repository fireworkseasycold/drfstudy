from rest_framework.viewsets import ModelViewSet
from .models import Student
from  .serializers import StudentschoolModelSerializer
# Create your views here.

class StudentModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentschoolModelSerializer