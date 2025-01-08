from django.contrib.auth.backends import BaseBackend
from safekey.models import Usuario

class AutenticandoUsuario(BaseBackend):
    def authenticate(self, request, email=None, senha=None):
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.senha == senha:
                return usuario
        except Usuario.DoesNotExist:
            return None

