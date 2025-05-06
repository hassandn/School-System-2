from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SchoolViewSet, CourseViewSet

router = DefaultRouter()
router.register('schools', SchoolViewSet)
router.register('courses', CourseViewSet)

urlpatterns = [

]
urlpatterns += router.urls
