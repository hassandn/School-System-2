from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from accounts.permissions import IsAdminPermission, IsTeacherOfClassPermission
from .models import School, Course, Class
from .serializers import SchoolSerializer, CourseSerializer, ClassSerializer, AddStudentSerializer


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
    permission_classes = [IsTeacherOfClassPermission]
    serializer_class = AddStudentSerializer

