from rest_framework import viewsets
from safekey.models import User, UserType, Room, Reservation, History
from safekey.serializers import UserSerializer, UsersTypesSerializer, CustomTokenObtainPairSerializer, RoomSerializer, ReservationSerializer, HistorySerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.decorators import action
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from setup.settings import URL_FRONTEND

# Criando ViewSet com todo o crud do meu modelo Usuario
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() # buscando todos os dados do meu usuário
    serializer_class = UserSerializer
            
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtém o usuário a ser deletado
        self.perform_destroy(instance)
        return Response({"detail": "Usuário deletado com sucesso"}, status=204)
    
    @action(detail=False, methods=['POST', 'PUT','PATCH','DELETE'])
    def listUsers(self, request):
        if request.method == 'POST':
            if isinstance(request.data, list):
                serializer = self.get_serializer(data=request.data, many=True)
                # Valida e salva os dados
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                return Response(serializer.data, status=201)
            return Response({"error": "Os dados devem ser uma lista"}, status=400)
            
        if request.method == 'PUT' or request.method == 'PATCH':
            if isinstance(request.data, list):
                instances = []
                errors = []

                for user_data in request.data:
                    user_id = user_data.get("id")
                    if not user_id:
                        errors.append({"error": "ID é obrigatório para atualizar", "data": user_data})
                        continue

                    try:
                        instance = User.objects.get(id=user_id)
                        serializer = self.get_serializer(instance, data=user_data, partial=True) # `partial=True` permite atualizações parciais
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        instances.append(serializer.data)
                    except User.DoesNotExist:
                        errors.append({"error": f"Usuário com ID {user_id} não encontrado."})

                if errors:
                    return Response({"updated": instances, "errors": errors}, status=207)  
                
                return Response(instances, status=200)
            return Response({"error": "Os dados devem ser uma lista"}, status=400)
        
        if request.method == 'DELETE':
            if isinstance(request.data, list):
                ids = [user.get("id") for user in request.data if "id" in user]  # Extrai apenas os IDs
                if ids:
                    User.objects.filter(id__in=ids).delete()
                    return Response({"detail": "Usuários deletados com sucesso"}, status=204)
                return Response({"error": "Nenhum ID válido fornecido"}, status=400)
            return Response({"error": "Os dados devem ser uma lista"}, status=400)

# Criando ViewSet com todo o crud do meu modelo TipoUsuario
class UsersTypesView(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UsersTypesSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtém o tipo do usuário a ser deletado
        self.perform_destroy(instance)
        return Response({"detail": "Tipo de usuário deletado com sucesso"}, status=204)

# Criando ViewSet para o login
class loginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Criando ViewSet para as salas
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtém a sala a ser deletada
        self.perform_destroy(instance)
        return Response({"detail": "Sala deletada com sucesso"}, status=204)
    
    @action(detail=False, methods=['POST','PUT','PATCH','DELETE'])
    def listRooms(self, request):
        if request.method == 'POST':
            if isinstance(request.data, list):
                serializer = self.get_serializer(data=request.data, many=True)
                # Valida e salva os dados
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                return Response(serializer.data, status=201)
            return Response({"error": "Os dados devem ser uma lista"}, status=400)
        
        if request.method == 'PUT' or request.method == 'PATCH':
            if isinstance(request.data, list):
                instances = []
                errors = []

                for room_data in request.data:
                    room_id = room_data.get("id")
                    if not room_id:
                        errors.append({"error": "ID é obrigatório para atualizar", "data": room_data})
                        continue

                    try:
                        instance = Room.objects.get(id=room_id)
                        serializer = self.get_serializer(instance, data=room_data, partial=True)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        instances.append(serializer.data)
                    except Room.DoesNotExist:
                        errors.append({"error": f"Sala com ID {room_id} não encontrado."})

                if errors:
                    return Response({"updated": instances, "errors": errors}, status=207)  
                
                return Response(instances, status=200)
            return Response({"error": "Os dados devem ser uma lista"}, status=400)
    
        if request.method == 'DELETE':
            if isinstance(request.data, list):
                ids = [room.get("id") for room in request.data if "id" in room]  # Extrai apenas os IDs
                if ids:
                    Room.objects.filter(id__in=ids).delete()
                    return Response({"detail": "Salas deletadas com sucesso"}, status=204)
                return Response({"error": "Nenhum ID válido fornecido"}, status=400)
            return Response({"error": "Os dados devem ser uma lista"}, status=400)

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
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtém a reserva a ser deletada
        self.perform_destroy(instance)
        return Response({"detail": "Reserva deletada com sucesso"}, status=204)

    def send_email_to_responsible(self, reservation):
        frontend_decision_url = f"{URL_FRONTEND}/decision/reservation/{reservation.id}"

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
    
    def send_reservation_status_update(self, reservation):
        # Envia a notificação via WebSocket para todos os clientes conectados
        channel_layer = get_channel_layer()
        message = f"Status da reserva {reservation.id} atualizado para {reservation.status}."
        async_to_sync(channel_layer.group_send)(
            "room_status_channel",  # O grupo do WebSocket
            {
                "type": "send_room_status_update",
                "message": message,
                "updated": "reservas"
            }
        )

    # Rota para aprovar uma reserva
    @action(detail=True, methods=['GET'])
    def approve(self, request, pk=None):
        reservation = self.get_object()
        
        if reservation.status in ["Aprovado", "Recusado"]:
            return Response({'detail': 'Essa reserva já foi processada.'}, status=400)

        reservation.status = "Aprovado"
        reservation.save()

        self.send_reservation_status_update(reservation)

        self.send_confirmation_email(reservation, 'Aprovada')

        return Response({'detail': 'Reserva aprovada com sucesso.'}, status=200)
        
    # Rota para recusar uma reserva
    @action(detail=True, methods=['GET'])
    def reject(self, request, pk=None):
        reservation = self.get_object()

        if reservation.status in ["Aprovado", "Recusado"]:
            return Response({'detail': 'Essa reserva já foi processada.'}, status=400)
        
        reservation.status = "Recusado"
        reservation.save()

        self.send_reservation_status_update(reservation)

        self.send_confirmation_email(reservation, 'Recusado')

        return Response({'detail': 'Reserva recusada com sucesso.'}, status=200)
    
    # Rota para buscar todas as reservas de um usuário
    @action(detail=True, methods=['GET'])
    def userReservations(self, request, pk=None):
        user = User.objects.get(id=pk)
        reservations = Reservation.objects.filter(user=user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=200)
    
    # Rota para buscar todas as reservas de uma sala
    @action(detail=True, methods=['GET'])
    def roomReservations(self, request, pk=None):
        room = Room.objects.get(id=pk)
        reservations = Reservation.objects.filter(room=room)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=200)
    
    @action(detail=False, methods=['DELETE'])
    def listReservations(self, request):
        if request.method == 'DELETE':
            if isinstance(request.data, list):
                ids = [reservation.get("id") for reservation in request.data if "id" in reservation]  # Extrai apenas os IDs
                if ids:
                    Reservation.objects.filter(id__in=ids).delete()
                    return Response({"detail": "Reservadas deletadas com sucesso"}, status=204)
                return Response({"error": "Nenhum ID válido fornecido"}, status=400)
            return Response({"error": "Os dados devem ser uma lista"}, status=400)

# Criando ViewSet para o historico(apenas visualização) 
class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtém o historico a ser deletado
        self.perform_destroy(instance)
        return Response({"detail": "Historico deletado com sucesso"}, status=204)
