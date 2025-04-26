from .serializers import UserSerializer, UserDetailSerializer, UserUpdateSerializer
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class UserListViewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class UserView(APIView):
    def get(self, request, pk=None):
        if pk:#it's detial view
            user = get_object_or_404(get_user_model(), pk=pk)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data)
        else:#it's list view
            users = get_list_or_404(get_user_model())
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
       
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        user = get_user_model().objects.get(pk=pk)
        serilizer = UserUpdateSerializer(user, data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        serilizer = UserUpdateSerializer(user, data=request.data, partial=True)        
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        serializer = UserSerializer
        if user.delete():
            return Response({"message: user deleted succesfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    