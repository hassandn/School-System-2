from .serializers import UserSerializer, UserDetailSerializer, UserUpdateSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOwnerPermission
from .filters import IsOwnerFilterBackend

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
            return [IsOwnerPermission()]
        elif self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return  UserUpdateSerializer
        return  UserSerializer            
            
    def destroy(self, request, *args, **kwargs):
         return Response(
            {"message": f"user {self.request.user.username} deleted!"},
            status=status.HTTP_204_NO_CONTENT
        )
