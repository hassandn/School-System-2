from datetime import timezone

from rest_framework import serializers
from django.contrib.auth import get_user_model
from school.models import School, Course, Class, Exercise, ExerciseAnswer, Announcement
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
        if attrs['exercise'].due_date >= timezone.now():
            if attrs['exercise'].classroom.students.filter(id=self.context['request'].user.id).exists():
                return attrs
            else:
                raise serializers.ValidationError("user must be student of class.")

        else:
            raise serializers.ValidationError("The deadline for submitting the exercise has passed.")


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

    def validate_classroom(self, value):
        if value.teacher.username == self.context['request'].user.username:
            return value
        else:
            raise serializers.ValidationError("کاربر معلم این کلاس نیست.")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['views'] = instance.viewed_by.count()
        del representation['viewed_by']
        representation['author'] = get_user_model().objects.get(pk=representation['author']).username
        representation['classroom'] = Class.objects.get(pk=representation['classroom']).class_name
        return representation

    

