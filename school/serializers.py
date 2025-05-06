from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from school.models import School, Course, Class


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
                
        
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

    def validate_students(self, value):
        for user in value:
            if not user.groups.filter(name="Student").exists():
                raise serializers.ValidationError(
                    f"user {user.username} is not student."
                )
        return value

    def validate_teacher(self, value):
        if not value.groups.filter(name="Teacher").exists():
            raise serializers.ValidationError(
                f"user {value.username} is not teacher."
            )
        return value


class AddStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['students']
        extra_kwargs = {'students': {'required': True}}

    def validate_students(self, value):
        for user in value:
            if not user.groups.filter(name="Student").exists():
                raise serializers.ValidationError(
                    f"user {user.username} is not student."
                )
        return value
