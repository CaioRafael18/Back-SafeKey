from rest_framework import viewsets
from safekey.models import User, UserType, Room, Reservation
from safekey.serializers import UserSerializer, UsersTypesSerializer, CustomTokenObtainPairSerializer, RoomSerializer, ReservationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from safekey.permissions.permissions_user import PermissionUser
from safekey.permissions.permissions_users_types import PermissionsUsersTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
    
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
    queryset = Reservation.objects.filter(deleted_at__isnull=True)
    serializer_class = ReservationSerializer

    def destroy(self, request, *args, **kwargs):
        # Obtém o objeto da reserva
        reservation = self.get_object()

        # Verifica se já foi deletado
        if reservation.deleted_at is not None:
            return Response({'detail': "A reserva já foi deletada."}, status=400)

        # Soft delete da reserva
        reservation.delete()  # Chamando o método delete() do modelo
        return Response({'detail': 'Reserva deletada com sucesso.'}, status=204)