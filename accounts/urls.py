from django.urls import path
from .views import UserCreateView, UserListView, UserUpdateView, UserDetailView

urlpatterns = [
    path('create-user/', UserCreateView.as_view(), name='user_create'),
    path('list-users/', UserListView.as_view(), name='user_lsit'),
    path('update-user/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/', UserDetailView.as_view(), name="user_detail")
]
