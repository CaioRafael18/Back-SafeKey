from celery import shared_task
from django.utils import timezone
from channels.layers import get_channel_layer
from .models import Reservation
import logging
from asgiref.sync import async_to_sync
logger = logging.getLogger(__name__)

@shared_task
def update_room_status_task():
    now_time = timezone.localtime(timezone.now()).time()
    now_date = timezone.localtime(timezone.now()).date()

    reservations = Reservation.objects.filter(
        status="Aprovado",
        date_schedulling=now_date
    )

    for reservation in reservations:
        # Verifica se a reserva está no horário de ocupação
        if reservation.start_time <= now_time <= reservation.end_time:
            # Durante o horário da reserva, marca a sala como "Ocupado"
            if reservation.room.status != "Ocupado":
                reservation.room.status = "Ocupado"
                reservation.room.save()
                send_client_status_update(reservation)
        # Verifica se a reserva já passou e atualiza o status da sala para "Disponivel"
        elif reservation.end_time < now_time:
            if reservation.room.status != "Disponivel":
                reservation.room.status = "Disponivel"
                reservation.room.save()
                send_client_status_update(reservation)

def send_client_status_update(reservation):
    # Envia a notificação via WebSocket para todos os clientes conectados
    channel_layer = get_channel_layer()
    message = f"Status da sala {reservation.room.name} atualizado para {reservation.room.status}."
    logger.info(f"Enviando mensagem para o grupo 'room_status_channel': {message}")

    async_to_sync(channel_layer.group_send)(
        "room_status_channel",  # O grupo do WebSocket
        {
            "type": "send_room_status_update",
            "message": message,
            "updated": "salas"
        }
    )