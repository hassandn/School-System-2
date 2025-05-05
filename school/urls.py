from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SchoolViewSet

router = DefaultRouter()
router.register('schools', SchoolViewSet)

urlpatterns = [

]
urlpatterns += router.urls
