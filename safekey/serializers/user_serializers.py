from rest_framework import serializers
from safekey.models import User, UserType
from django.contrib.auth.hashers import make_password
from safekey.serializers.user_types_serializers import UsersTypesSerializer

class UserSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=UserType.objects.all())  # Para POST, aceita apenas o ID do type

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'type']

    def create(self, validated_data):
        # Armazenando a senha do usuário criado como hash no banco
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def to_representation(self, instance):
        # retorna o objeto completo do tipo de usuário (com id e type)
        representation = super().to_representation(instance)
        representation['type'] = UsersTypesSerializer(instance.type).data
        return representation