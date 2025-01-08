from rest_framework import serializers
from safekey.models import Usuario, TipoUsuario

class UsuarioSerializer(serializers.ModelSerializer):
    # Definindo o modelo usuário e pegando todos os campos
    class Meta:
        model = Usuario
        fields = '__all__'

class TiposUsuariosSerializer(serializers.ModelSerializer):
    idUsuario = serializers.IntegerField(source='usuario.id')  # Extrai apenas o ID do usuário
    nome = serializers.CharField(source='usuario.nome')  # Extrai apenas o nome do usuário
    tipo = serializers.CharField(source='usuario.tipo')  # Extrai apenas o tipo do usuário

    class Meta:
        model = TipoUsuario
        fields = ['id', 'idUsuario', 'nome', 'tipo']
