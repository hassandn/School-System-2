from .serializers import UserSerializer, UserDetailSerializer, UserUpdateSerializer
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerPermission

class UserListViewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

class UserView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    pagination_class = UserListViewPagination

    def get_permissions(self):
        if self.action in ['retrieve', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [IsOwnerPermission]
        elif self.action == 'create':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        if self.action == 'retrieve':
            return UserDetailSerializer
        return  UserSerializer            
            

