from rest_framework import viewsets
from safekey.models import Usuario, TipoUsuario
from safekey.serializers import UsuarioSerializer, TiposUsuariosSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from safekey.permissoes.permissao_usuario import PermissaoUsuarios
from safekey.permissoes.permissao_tipos_usuario import PermissaoTiposUsuarios
from rest_framework.permissions import IsAuthenticated
    
# Criando ViewSet com todo o crud do meu modelo Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, PermissaoUsuarios] 
    queryset = Usuario.objects.all() # buscando todos os dados do meu usuário
    serializer_class = UsuarioSerializer

# Criando ViewSet com todo o crud do meu modelo TipoUsuario
class TiposUsuariosView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, PermissaoTiposUsuarios] 
    queryset = TipoUsuario.objects.all()
    serializer_class = TiposUsuariosSerializer

# Criando ViewSet para o login
class loginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer