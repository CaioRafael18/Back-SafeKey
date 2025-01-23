from django.contrib.auth.backends import BaseBackend
from safekey.models import User

class AuthenticationUser(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.password == password:
                return user
        except user.DoesNotExist:
            return None

