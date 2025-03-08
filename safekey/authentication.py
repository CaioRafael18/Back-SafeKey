from django.contrib.auth.backends import BaseBackend
from safekey.models.user_models import User
from django.contrib.auth.hashers import check_password

class AuthenticationUser(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            # Verificando a hash salva no banco
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None

