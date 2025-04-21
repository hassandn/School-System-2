from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

class UserCreateView(generics.CreateAPIView):
    """API view to create a new student user."""
    serializer_class = UserSerializer


# class StudentListView
