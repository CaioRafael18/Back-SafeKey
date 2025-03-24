from celery import shared_task
from django.utils import timezone
from ..models import Reservation
from safekey.services.websocket_service import WebSocketService

@shared_task(name='safekey.tasks.tasks.update_status_task')
def update_status_task():
    now_time = timezone.localtime(timezone.now()).time()
    now_date = timezone.localtime(timezone.now()).date()

    reservations = Reservation.objects.filter(
        status="Aprovado",
        date_schedulling=now_date
    )

    for reservation in reservations:
        # Pula a reserva sem 'end_time'        
        if reservation.end_time is None:
            continue

        if reservation.start_time <= now_time <= reservation.end_time:
            # Atualiza status baseado no horário de ocupação
            update_room_status(reservation, now_time)

        # Verifica se a reserva já passou
        if reservation.end_time < now_time:
            close_reservation(reservation)

# Atualiza o status da sala durante o horário da reserva
def update_room_status(reservation, now_time):
    if reservation.room.status == "Disponivel":
        set_room_status(reservation.room, "Reservada", "sala")
    elif reservation.room.status == "Reservada" and reservation.room.status_key == "Retirada":
        set_room_status(reservation.room, "Ocupado", "sala")
    
# Marca a sala como disponível e encerra a reserva se já passou 
def close_reservation(reservation):
    if reservation.room.status != "Disponivel":
        set_room_status(reservation.room, "Disponivel", "sala")
        reservation.status = "Encerrado"
        reservation.save()

# Define o status da sala e envia a atualização via WebSocket
def set_room_status(room, status, websocket_type):
    room.status = status
    room.save()
    WebSocketService.send_type_status_update(room, websocket_type)