from rest_framework.permissions import BasePermission

class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk

class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Admin').exists()
