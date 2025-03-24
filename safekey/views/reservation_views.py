from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from safekey.models import Reservation, User, Room
from safekey.serializers.reservation_serializers import ReservationSerializer
from safekey.services.email_service import EmailService
from safekey.services.websocket_service import WebSocketService
from setup.settings import URL_FRONTEND
from rest_framework.permissions import AllowAny

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.filter(deleted_at__isnull=True)
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        # Salva a reserva no banco
        reservation = serializer.save()  
        
        # Envia um e-mail para o responsável
        if reservation.responsible is not None:
            try:
                frontend_decision_url = f"{URL_FRONTEND}/decision/reservation/{reservation.id}"
                EmailService.send_responsible_email(reservation, frontend_decision_url)
            except Exception as e:
                reservation.delete()
                raise ValidationError({'detail': f'Erro ao enviar e-mail: {str(e)}'})
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtém a reserva a ser deletada
        self.perform_destroy(instance)
        return Response({"detail": "Reserva deletada com sucesso"}, status=204)    

    def update_reservation_status(self, reservation, status, user):
        if reservation.status in ["Aprovado", "Recusado"]:
            return Response({'detail': 'Essa reserva já foi processada.'}, status=400)
        
        # Se o usuário for publico, atualiza o status da chave e da sala
        if user == "public":
            room = Room.objects.get(id=reservation.room.id)
            room.status = "Ocupado"
            room.status_key = "Retirada"
            room.save()
        
        reservation.status = status
        reservation.save()
        WebSocketService.send_type_status_update(reservation, "reserva")
        EmailService.send_reservation_email(reservation, status)
        return Response({'detail': f'Reserva {status.lower()} com sucesso.'}, status=200)
    
    # Rota para aprovar uma reserva
    @action(detail=True, methods=['GET','POST'], permission_classes=[AllowAny])
    def approve(self, request, pk=None):
        reservation = self.get_object()

        # Se for POST, verifica se está vindo o "public"
        if request.method == "POST":
            user = request.data.get("user", None)

            if user != "public":
                return Response({"detail": "Autenticação necessária."}, status=401)
        # Se for GET, exige autenticação normal
        else:
            if not request.user.is_authenticated:
                return Response({"detail": "Autenticação necessária."}, status=401)
            user = request.user 

        return self.update_reservation_status(reservation, "Aprovado", user)
        
    # Rota para recusar uma reserva
    @action(detail=True, methods=['GET'])
    def reject(self, request, pk=None):
        reservation = self.get_object()
        return self.update_reservation_status(reservation, "Recusado")
    
    # Rota para devolver uma chave
    @action(detail=True, methods=['GET'], permission_classes=[AllowAny])
    def return_key(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = "Encerrado"
        reservation.save()

        room = Room.objects.get(id=reservation.room.id)
        room.status = "Disponivel"
        room.status_key = "Disponivel"
        room.save()
        return Response({'detail': 'Chave devolvida com sucesso.'}, status=200)
    
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
    
    # Rota para deletar várias reservas
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