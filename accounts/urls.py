from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('create-user/', UserCreateView.as_view(), name='user_create'),
]
