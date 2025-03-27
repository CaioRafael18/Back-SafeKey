from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from safekey.models import Reservation, User, Room
from safekey.views.room_views import RoomViewSet
from safekey.serializers.reservation_serializers import ReservationSerializer
from safekey.services.email_service import EmailService
from safekey.services.websocket_service import WebSocketService
from rest_framework.permissions import AllowAny
from setup.settings import URL_FRONTEND

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

    # Rota para atualizar status da reserva
    def update_reservation_status(self, reservation, status):
        if reservation.status in ["Aprovado", "Recusado"]:
            return Response({'detail': 'Essa reserva já foi processada.'}, status=400)
        
        reservation.status = status
        reservation.save()
        WebSocketService.send_type_status_update(reservation, "reserva")
        EmailService.send_reservation_email(reservation, status)
        return Response({'detail': f'Reserva {status.lower()} com sucesso.'}, status=200)
    
    # Rota para aprovar uma reserva
    @action(detail=True, methods=['GET'])
    def approve(self, request, pk=None):
        reservation = self.get_object()
        return self.update_reservation_status(reservation, "Aprovado")
    
    # Rota para recusar uma reserva
    @action(detail=True, methods=['GET'])
    def reject(self, request, pk=None):
        reservation = self.get_object()
        return self.update_reservation_status(reservation, "Recusado")
    
    # Rota para buscar todas as reservas de um usuário
    @action(detail=True, methods=['GET'])
    def user_reservations(self, request, pk=None):
        user = User.objects.get(id=pk)
        reservations = Reservation.objects.filter(user=user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=200)
    
    # Rota para buscar todas as reservas de uma sala
    @action(detail=True, methods=['GET'])
    def room_reservations(self, request, pk=None):
        room = Room.objects.get(id=pk)
        reservations = Reservation.objects.filter(room=room)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=200)
    
    # Rota publica para exibir todas as reservas
    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def public(self, request, pk=None):
        reservation = Reservation.objects.all()
        serializer = ReservationSerializer(reservation, many=True)
        return Response(serializer.data)
    
    # Rota publica para remover uma chave
    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def remove_key(self, request):
        serializer = self.get_serializer(data=request.data)
        
        # Se for válido Salva a reserva no banco
        if serializer.is_valid():
            reservation = serializer.save() 
            room = Room.objects.get(id=reservation.room.id)
            
            RoomViewSet.update_room_status(room, "Ocupado", "Retirada")
            return Response({"detail": "Chave retirada com sucesso."}, status=200)
        return Response(serializer.errors, status=400)

    # Rota publica para devolver uma chave
    @action(detail=True, methods=['PATCH'], permission_classes=[AllowAny])
    def return_key(self, request, pk=None):
        reservation = self.get_object()
        
        # Se for válido atualiza os dados da reserva com os dados enviados pelo front
        serializer = self.get_serializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save() 
            room = Room.objects.get(id=reservation.room.id)
            
            RoomViewSet.update_room_status(room, "Disponível", "Disponível")
            return Response({"detail": "Chave devolvida com sucesso."}, status=200)
        return Response(serializer.errors, status=400)
    
    # Rota para deletar várias reservas
    @action(detail=False, methods=['DELETE'])
    def list_reservations(self, request):
        if request.method == 'DELETE':
            if isinstance(request.data, list):
                ids = [reservation.get("id") for reservation in request.data if "id" in reservation]  # Extrai apenas os IDs
                if ids:
                    Reservation.objects.filter(id__in=ids).delete()
                    return Response({"detail": "Reservadas deletadas com sucesso"}, status=204)
                return Response({"error": "Nenhum ID válido fornecido"}, status=400)
            return Response({"error": "Os dados devem ser uma lista"}, status=400)