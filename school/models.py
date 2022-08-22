from django.db import models

# Create your models here.
from django.utils import timezone

"""
学生 sch_student           1
成绩 sch_achievement       n    n
课程 sch_course                 1    n
老师 sch_teacher                     1
"""


class Student(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    age = models.SmallIntegerField(verbose_name="年龄")
    sex = models.BooleanField(default=False)

    class Meta:
        db_table = "sch_student"

    def __str__(self):
        return self.name

    #自定义模型方法
    @property  #可以不带这个属性方法
    def achievement(self):
        """序列化器嵌套写法4 """
        # cj=self.s_achievement.values()  #不能all()会报错 ，使用values()直接获取字典 s_achievement为从表对应外键字段,也可以在values()里指定字段
        # ret=[{"score": item.score, "course": item.course.name, "teacher": item.course.teacher.teacher.name} for item in cj]
        # 在values()里指定某些字段
        ret=self.s_achievement.values("student__name","course__name","course__teacher__name","score")
        return  ret




class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name="课程名称")
    teacher = models.ForeignKey('Teacher', on_delete=models.DO_NOTHING, related_name="course", db_constraint=False)  #to是指向你的表，带上引号你关联的表位置可以在此表之后，不带关联的表就必须在前

    class Meta:
        db_table = 'sch_course'

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    sex = models.BooleanField(default=False)

    class Meta:
        db_table = 'sch_teacher'

    def __str__(self):
        return self.name


class Achievement(models.Model):
    score = models.DecimalField(default=0, max_digits=4, decimal_places=1, verbose_name="成绩")
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, related_name='s_achievement', db_constraint=False) #db_constraint=False 把关联切断,但保留连表查询的功能，是虚拟外键，提高mysql效率；related_name子表在主表中对应的外键属性，DO_NOTHING表示删除互相不做操作
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name="c_achievement", db_constraint=False)
    create_dtime = models.DateTimeField(auto_created=timezone.now)

    class Meta:
        db_table = 'sch_achievement'

    def __str__(self):
        return str(self.score)  #__str__ returned non-string (type decimal.Decimal)

