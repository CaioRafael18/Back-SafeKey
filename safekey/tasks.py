from celery import shared_task
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync  # Import necessário
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
            send_all_reservations_to_client(reservations)

# Função para enviar todas as reservas para o front-end (completa)
def send_all_reservations_to_client(reservations):
    channel_layer = get_channel_layer()

    # Criação de um dicionário com todas as reservas
    all_reservations = [
        {
            "room_name": reservation.room.name,
            "status": reservation.room.status,
            "reservation_id": reservation.id,
            "start_time": reservation.start_time,
            "end_time": reservation.end_time,
            "date_schedulling": reservation.date_schedulling
        }
        for reservation in reservations
    ]

    # Envia para o WebSocket todas as reservas
    async_to_sync(channel_layer.group_send)(
        "room_status_channel",
        {
            "type": "send_room_status_update",
            "reservations": all_reservations
        }
    )