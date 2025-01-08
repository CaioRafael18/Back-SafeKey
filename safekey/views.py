from rest_framework import viewsets
from safekey.models import Usuario, TipoUsuario
from safekey.serializers import UsuarioSerializer, TiposUsuariosSerializer

# Criando ViewSet com todo o crud do meu modelo Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all() # buscando todos os dados do meu usuário
    serializer_class = UsuarioSerializer

    def perform_create(self, serializer):
        usuario = serializer.save() # salva o Usuario e retorna o objeto salvo
        TipoUsuario.objects.create(usuario=usuario)  # Associando corretamente o usuário ao TipoUsuario

# Criando ViewSet para a request do tipo Get
class TiposUsuariosView(viewsets.ReadOnlyModelViewSet):
    queryset = TipoUsuario.objects.all()
    serializer_class = TiposUsuariosSerializer
