from traceback import print_tb

from django.http import HttpResponse
from django.utils.dateparse import parse_time
from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from accounts.permissions import IsAdminPermission, IsTeacherOfClassPermission, IsTecherPermission
from .models import School, Course, Class, Exercise, ExerciseAnswer, Announcement
from .serializers import SchoolSerializer, CourseSerializer, ClassSerializer, AddStudentSerializer, ExerciseSerializer, \
    ExerciseAnswerSerializer, AnnouncementSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SchoolSerializer
    queryset = School.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            self.permission_classes = [IsAdminPermission]
        return super(SchoolViewSet, self).get_permissions()


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            self.permission_classes = [IsAdminPermission]
        return super(CourseViewSet, self).get_permissions()


class ClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Class.objects.all()
    serializer_class = ClassSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            self.permission_classes = [IsAdminPermission]
        return [permission() for permission in self.permission_classes]


class AddStudentToClass(generics.UpdateAPIView):
    queryset = Class.objects.all()
    permission_classes = [IsTeacherOfClassPermission | IsAdminPermission]
    serializer_class = AddStudentSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExerciseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminPermission | IsAuthenticated]
        [permission() for permission in self.permission_classes]


class ExerciseAnswerViewSet(viewsets.ModelViewSet):
    queryset = ExerciseAnswer.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExerciseAnswerSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'create']:
            self.permission_classes = [IsTecherPermission | IsAdminPermission]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def retrieve(self, request, *args, **kwargs):
        announcement_id = self.kwargs.get('pk')
        class_id = Announcement.objects.get(pk=announcement_id).classroom.id
        classroom = Class.objects.get(pk=class_id)
        if classroom.students.filter(pk=self.request.user.pk).exists():
            announcement = Announcement.objects.get(pk=announcement_id)
            announcement.viewed_by.add(self.request.user)
        return super(AnnouncementViewSet, self).retrieve(request, *args, **kwargs)

