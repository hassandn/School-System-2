from django.urls import path
from .views import UserView, NearestSchool
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserView)


urlpatterns = [
    path('token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('nearest-schools/',NearestSchool.as_view(), name='nearest_schools'),
]
urlpatterns += router.urls