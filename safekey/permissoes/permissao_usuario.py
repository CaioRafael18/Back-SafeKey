from rest_framework.permissions import BasePermission

class PermissaoUsuarios(BasePermission):

    def has_permission(self, request, view):
        acesso = ['Administrador']
        tipoUsuario = request.auth.payload['tipoUsuario']
        return tipoUsuario in acesso
