from django.urls import path
from .views import UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('create-user/', UserView.as_view(), name='user_create'),
    path('list-users/', UserView.as_view(), name='user_lsit'),
    path('update-user/<int:pk>/', UserView.as_view(), name='user_update'),
    path('user/<int:pk>/', UserView.as_view(), name="user_detail"),
    path('delete/user/<int:pk>/', UserView.as_view(), name="user_delete"),
]
