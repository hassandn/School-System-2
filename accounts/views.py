from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination


class UserListViewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class UserCreateView(generics.CreateAPIView, mixins.CreateModelMixin):
    """API view to create a new student user."""
    serializer_class = UserSerializer


class UserUpdateView(generics.UpdateAPIView, mixins.UpdateModelMixin):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    
    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)


class UserListView(generics.ListAPIView, mixins.ListModelMixin):
    """API view for users list view"""
    serializer_class = UserSerializer
    pagination_class = UserListViewPagination
    queryset = get_user_model().objects.filter(registration_status="Registered")


class UserDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
        
    
