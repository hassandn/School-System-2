from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


from .views import SchoolViewSet, CourseViewSet, ClassViewSet, AddStudentToClass, ExerciseViewSet, ExerciseAnswerViewSet, AnnouncementViewSet

router = DefaultRouter()
router.register('schools', SchoolViewSet)
router.register('courses', CourseViewSet)
router.register('classes', ClassViewSet)
router.register('exercises', ExerciseViewSet)
router.register('submit-answer', ExerciseAnswerViewSet)
router.register('announcement', AnnouncementViewSet)
urlpatterns = [
    path('class/<int:pk>/addstudents/', AddStudentToClass.as_view(), name='add_student_to_class'),
]
urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
