from django.db import models


# Create your models here.
#create database students charset=utf8mb4;
class Student(models.Model):
    """学生信息"""
    name = models.CharField(max_length=100, verbose_name='姓名',help_text='学生姓名')  #help_text用于接口文档显示
    sex = models.BooleanField(default=1, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄',help_text="年龄不能小于0")
    classmate = models.CharField(max_length=5, verbose_name='班级编号')
    description = models.TextField(max_length=1000, verbose_name='个性签名')

    class Meta:
        db_table = 'tb_student'
        verbose_name = '学生'
        verbose_name_plural = verbose_name
