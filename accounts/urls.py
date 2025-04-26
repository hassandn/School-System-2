from django.urls import path
from .views import UserView

urlpatterns = [
    path('create-user/', UserView.as_view(), name='user_create'),
    path('list-users/', UserView.as_view(), name='user_lsit'),
    path('update-user/<int:pk>/', UserView.as_view(), name='user_update'),
    path('user/<int:pk>/', UserView.as_view(), name="user_detail")
]
