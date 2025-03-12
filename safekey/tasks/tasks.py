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
        # Verifica se a reserva está no horário de ocupação
        if reservation.start_time <= now_time <= reservation.end_time:
            # Marca a sala como "Reservada"
            if reservation.room.status == "Disponivel":
                reservation.room.status = "Reservada"
                reservation.room.save()
                WebSocketService.send_type_status_update(reservation.room, "sala")
            # Durante o horário da reserva, marca a sala como "Ocupado" e a chave como "Retirada"
            elif reservation.room.status == "Reservada" and reservation.room.status_key == "Retirada":
                    reservation.room.status = "Ocupado"
                    reservation.room.save()
                    WebSocketService.send_type_status_update(reservation.room, "sala")
        # Verifica se a reserva já passou e atualiza o status da sala para "Disponivel" e o da reserva para "Encerrado"
        elif reservation.end_time < now_time:
            if reservation.room.status != "Disponivel":
                reservation.room.status = "Disponivel"
                reservation.room.save()
                reservation.status = "Encerrado"
                reservation.save()
                WebSocketService.send_type_status_update(reservation.room, "sala")
