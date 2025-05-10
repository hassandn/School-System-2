from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SchoolViewSet, CourseViewSet, ClassViewSet, AddStudentToClass, ExerciseViewSet

router = DefaultRouter()
router.register('schools', SchoolViewSet)
router.register('courses', CourseViewSet)
router.register('classes', ClassViewSet)
router.register('exercises', ExerciseViewSet)
urlpatterns = [
    path('class/<int:pk>/addstudents/', AddStudentToClass.as_view(), name='add_student_to_class'),
]
urlpatterns += router.urls
