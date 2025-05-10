from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model


class School(models.Model):
    school_name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    location = models.PointField( blank=False, null=False)
    
    def __str__(self):
        return f"{self.school_name}"


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    credits = models.PositiveSmallIntegerField()
    description = models.TextField()
    
    def __str__(self):
        return f"{self.course_name} - {self.credits}"


class Class(models.Model):
    class_name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(to=Course, on_delete=models.PROTECT)
    teacher = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='teacher_class')
    students = models.ManyToManyField(to=get_user_model(), blank=True, related_name='student_class')
    
    def __str__(self):
        return f"{self.class_name} - {self.course} - {self.teacher}"
    
    
class Exercise(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    classroom = models.ForeignKey(to=Class, on_delete=models.PROTECT)
    teacher = models.ForeignKey(to=get_user_model(), on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.classroom} - {self.title[:15]}"




