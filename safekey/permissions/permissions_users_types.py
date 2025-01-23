from rest_framework.permissions import BasePermission

class PermissionsUsersTypes(BasePermission):
    def has_permission(self, request, view):
        access = ['Administrador']
        type_user = request.auth.payload['typeUser']
        return type_user in access
