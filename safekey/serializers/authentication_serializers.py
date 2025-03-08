from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from safekey.models import UserType
from safekey.serializers.user_serializers import UserSerializer
from safekey.serializers.user_types_serializers import UsersTypesSerializer

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        # Se não encontrar o usuário(retornar None)
        if not user:
            raise AuthenticationFailed({'detail': 'Credenciais inválidas. Verifique seu e-mail e senha.'})

        # Criando token e refresh token
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['userType'] = user.type.type

        # Se o usuário for autenticado com sucesso, retorne os dados necessários
        user_serializer = UserSerializer(user)
        id_type = user_serializer.data['type']['id']
        type_object = UserType.objects.get(id=id_type)
        user_type_serializer = UsersTypesSerializer(type_object)

        # Substituir o campo 'type' no user_serializer.data com os dados completos do 'user_type_serializer.data'
        user_data = user_serializer.data
        user_data['type'] = user_type_serializer.data

        return {
            'refresh_token': str(refresh_token),
            'access_token': str(access_token),
            'user': user_data,
        }