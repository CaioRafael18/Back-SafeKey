from rest_framework.permissions import BasePermission

class PermissionUser(BasePermission):

    def has_permission(self, request, view):
        access = ['Administrador']
        user_type = request.auth.payload['userType']
        return user_type in access

