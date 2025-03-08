from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now

# Gerenciador para o modelo User
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)  # Usa o método set_password para garantir que a senha seja criptografada
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Modelo de usuário personalizado
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, blank=False, unique=True)  # Nome do usuário
    email = models.EmailField(max_length=40, blank=False, unique=True)  # Email do usuário
    password = models.CharField(max_length=128, blank=False)  # Senha do usuário
    type = models.ForeignKey('UserType', on_delete=models.CASCADE)  # Tipo de usuário

    is_active = models.BooleanField(default=True)  # Campo para verificar se o usuário está ativo
    is_staff = models.BooleanField(default=False)  # Campo para verificar se o usuário é um staff
    date_joined = models.DateTimeField(default=now)

    # Gerenciador para o modelo User
    objects = CustomUserManager()

    # Usado para autenticação do usuário
    USERNAME_FIELD = 'email'  # Pode ser 'email' ou 'name', dependendo da sua preferência
    REQUIRED_FIELDS = ['name']  # Campos obrigatórios para criar um superusuário

    def __str__(self):
        return self.name