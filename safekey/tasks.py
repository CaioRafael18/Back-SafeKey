from celery import shared_task
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync 
from .models import Reservation

@shared_task
def update_room_status_task():
    now_time = timezone.localtime(timezone.now()).time()
    now_date = timezone.localtime(timezone.now()).date()

    reservations = Reservation.objects.filter(
        status="Aprovado",
        date_schedulling=now_date
    )

    for reservation in reservations:
        room = reservation.room  # Evita acessos desnecessários ao banco

        # Atualiza status da sala
        novo_status = None
        if reservation.start_time <= now_time <= reservation.end_time:
            if room.status != "Ocupado":
                novo_status = "Ocupado"
        elif reservation.end_time < now_time:
            if room.status != "Disponivel":
                novo_status = "Disponivel"

        # Apenas salva e envia notificação se houver mudança de status
        if novo_status and room.status != novo_status:
            room.status = novo_status
            room.save()
            send_client_room_status_update(room.id, novo_status)

# Função para enviar mensagem WebSocket corretamente
def send_client_room_status_update(room_id, status):
    channel_layer = get_channel_layer()
    message = f"Status da sala {room_id} atualizado para {status}."

    async_to_sync(channel_layer.group_send)(
        "room_status_channel",  # Nome do grupo WebSocket correto
        {
            "type": "send_room_status_update",
            "message": message,
            "updated" : "salas"
        }
    )
