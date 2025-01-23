from rest_framework import viewsets
from safekey.models import User, UserType, Room, Reservation
from safekey.serializers import UserSerializer, UsersTypesSerializer, CustomTokenObtainPairSerializer, RoomSerializer, ReservationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from safekey.permissions.permissions_user import PermissionUser
from safekey.permissions.permissions_users_types import PermissionsTypesUsers
from rest_framework.permissions import IsAuthenticated
    
# Criando ViewSet com todo o crud do meu modelo Usuario
class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, PermissionUser] 
    queryset = User.objects.all() # buscando todos os dados do meu usuário
    serializer_class = UserSerializer

# Criando ViewSet com todo o crud do meu modelo TipoUsuario
class UsersTypesView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, PermissionsTypesUsers] 
    queryset = UserType.objects.all()
    serializer_class = UsersTypesSerializer

# Criando ViewSet para o login
class loginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer