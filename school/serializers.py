import datetime
from datetime import timezone
from traceback import print_tb

from django.contrib.auth.models import Group
from django.utils.http import escape_leading_slashes
from rest_framework import serializers
from django.contrib.auth import get_user_model
from school.models import School, Course, Class, Exercise, ExerciseAnswer
from django.utils import timezone

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


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        exclude = ['date_created', 'date_updated', 'teacher']

    def validate(self, attrs):
        user = self.context['request'].user
        if user.groups.filter(name="Teacher").exists():
            return attrs
        else:
            raise serializers.ValidationError("user must be teacher.")

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['teacher'] = user
        return super().create(validated_data)


class ExerciseAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseAnswer
        fields = '__all__'

    def validate_file(self, value):
        file_extension = str(value.name).split('.')[1]
        if file_extension in ['zip', 'pdf']:
            return value
        else:
            raise serializers.ValidationError("file must be zip or pdf.")

    def validate(self, attrs):
        print(attrs['exercise'].due_date)
        if attrs['exercise'].due_date >= timezone.now():
            return  attrs
        else:
            raise serializers.ValidationError("The deadline for submitting the exercise has passed.")
