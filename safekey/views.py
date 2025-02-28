from rest_framework import viewsets, status
from safekey.models import User, UserType, Room, Reservation, History
from safekey.serializers import UserSerializer, UsersTypesSerializer, CustomTokenObtainPairSerializer, RoomSerializer, ReservationSerializer, HistorySerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from safekey.permissions.permissions_user import PermissionUser
from safekey.permissions.permissions_users_types import PermissionsUsersTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.decorators import action
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from django.conf import settings

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

    def perform_create(self, serializer):
        # Salva a reserva no banco
        reservation = serializer.save()  
        
        # Envia um e-mail para o responsável
        if reservation.responsible is not None:
            try:
                self.send_email_to_responsible(reservation)
            except Exception as e:
                reservation.delete()
                raise ValidationError({'detail': f'Erro ao enviar e-mail: {str(e)}'})

    def send_email_to_responsible(self, reservation):
        frontend_decision_url = f"http://98.81.255.202:90/decision/reservation/{reservation.id}"

        # Envia e-mail ao responsável pela aprovação da reserva
        subject = "Reserva Pendente para Aprovação"
        message = (
            f"Olá {reservation.responsible.name},\n\n"
            f"O aluno {reservation.user.name} solicitou uma reserva para a sala {reservation.room.name}.\n"
            f"Data: {reservation.date_schedulling}\n"
            f"Horário: {reservation.start_time} - {reservation.end_time}\n"
            f"Motivo: {reservation.reason}\n\n"
            f"Acesse o link abaixo:\n"
            f"Link: {frontend_decision_url}\n"
        )

        context = {
            'responsible_name': reservation.responsible.name,
            'user_name': reservation.user.name,
            'room_name': reservation.room.name,
            'date_schedulling': reservation.date_schedulling,
            'start_time': reservation.start_time,
            'end_time': reservation.end_time,
            'reason': reservation.reason,
            'link_decision': frontend_decision_url,
        }

        html_message = render_to_string('reservation_email.html', context)
            
        send_mail(
            subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[reservation.responsible.email],
            html_message=html_message,
            fail_silently=False,
        )

    def send_confirmation_email(self, reservation, status):
        try:
            subject = f"Reserva {status}"
            message = (f"Olá {reservation.user.name},\n"
                       f"Sua reserva para a sala {reservation.room.name} foi {status.lower()}.\n")

            send_mail(
                subject,
                message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[reservation.user.email],
                fail_silently=False,
            )
        except Exception as e:
            raise ValidationError({'detail': f'Erro ao enviar confirmação de e-mail: {str(e)}'})

    def generate_action_link(self, reservation, action):
        return self.request.build_absolute_uri(
            f"/reservations/{reservation.id}/{action}/"
        )

    def destroy(self, request, *args, **kwargs):
        # Obtém o objeto da reserva
        reservation = self.get_object()

        # Verifica se já foi deletado
        if reservation.deleted_at is not None:
            return Response({'detail': "A reserva já foi deletada."}, status=400)

        # Soft delete da reserva
        try:
            reservation.delete()  
        except Exception as e:
            return Response({'detail': f'Erro ao deletar a reserva: {str(e)}'}, status=500)

        return Response({'detail': 'Reserva deletada com sucesso.'}, status=204)
    
    @action(detail=True, methods=['get'])
    def approve(self, request, pk=None):
        reservation = self.get_object()
        
        if reservation.status in ["Aprovado", "Recusado"]:
            return Response({'detail': 'Essa reserva já foi processada.'}, status=400)

        reservation.status = "Aprovado"
        reservation.save()

        self.send_confirmation_email(reservation, 'Aprovada')

        return Response({'detail': 'Reserva aprovada com sucesso.'}, status=200)
        
    @action(detail=True, methods=['get'])
    def reject(self, request, pk=None):
        reservation = self.get_object()

        if reservation.status in ["Aprovado", "Recusado"]:
            return Response({'detail': 'Essa reserva já foi processada.'}, status=400)
        
        reservation.status = "Recusado"
        reservation.save()

        self.send_confirmation_email(reservation, 'Recusado')

        return Response({'detail': 'Reserva recusada com sucesso.'}, status=200)
    
# Criando ViewSet para o historico(apenas visualização) 
class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
