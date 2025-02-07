from rest_framework import viewsets, status
from safekey.models import User, UserType, Room, Reservation, History
from safekey.serializers import UserSerializer, UsersTypesSerializer, CustomTokenObtainPairSerializer, RoomSerializer, ReservationSerializer, HistorySerializer
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

    def create(self, request, *args, **kwargs):
        # Verifica se os dados recebidos são uma lista
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        # Valida e salva os dados
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Criando ViewSet com todo o crud do meu modelo TipoUsuario
class UsersTypesView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, PermissionsTypesUsers] 
    queryset = UserType.objects.all()
    serializer_class = UsersTypesSerializer

# Criando ViewSet para o login
class loginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Criando ViewSet para as salas
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        # Verifica se os dados recebidos são uma lista
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        # Valida e salva os dados
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Criando ViewSet para as reservas
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
    
# Criando ViewSet para o historico(apenas visualização) 
class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
