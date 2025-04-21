from django.urls import path
from .views import UserCreateView, UserListView

urlpatterns = [
    path('create-user/', UserCreateView.as_view(), name='user_create'),
    path('list-users/',UserListView.as_view(), name='user_lsit'),
]
