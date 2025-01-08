from rest_framework.permissions import BasePermission

class GerenciaPermissoes(BasePermission):
    def permissao_aluno(self, request, view):
        return request.user.is_authenticated and request.user.tipo.tipo == 'Aluno'
    
    def permissao_aluno(self, request, view):
        return request.user.is_authenticated and request.user.tipo.tipo == 'Administrador'

    def permissao_aluno(self, request, view):
        return request.user.is_authenticated and request.user.tipo.tipo == 'Professor'