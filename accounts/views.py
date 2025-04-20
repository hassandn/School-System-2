from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import StudentSerializer

User = get_user_model()
class StudentCreateView(generics.CreateAPIView):
    """    API view to create a new student user."""
    serializer_class = StudentSerializer

