from rest_framework import serializers
from safekey.models import Usuario, TipoUsuario
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UsuarioSerializer(serializers.ModelSerializer):
    # Definindo o modelo usuário e pegando todos os campos
    class Meta:
        model = Usuario
        fields = '__all__'

class TiposUsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoUsuario
        fields = '__all__'

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        senha = attrs.get('senha')

        # Verificando autenticação do usuário
        usuario = authenticate(request=self.context.get('request'), email=email, senha=senha)

        # Se o usuário não existe
        if usuario is None:
            raise serializers.ValidationError("Credenciais inválidas.")
        
        # Criando token e refresh token
        refresh_token = RefreshToken.for_user(usuario)
        access_token = refresh_token.access_token

        # Se o usuário for autenticado com sucesso, retorne os dados necessários
        usuario_serializer = UsuarioSerializer(usuario)
        return {
            'refresh_token': str(refresh_token),
            'access_token': str(access_token),
            'usuario': usuario_serializer.data
        }
