from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

class UserCreateView(generics.CreateAPIView):
    """API view to create a new student user."""
    serializer_class = UserSerializer


class UserListView(generics.UpdateAPIView):
    pass
    

class UserListView(generics.ListAPIView):
    """API view for users list view"""
    serializer_class = UserSerializer
    queryset = get_user_model().objects.filter(registration_status="Registered")
    

