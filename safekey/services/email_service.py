from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class EmailService:
    def send_email(subject, message, recipient_list, html_message=None):
        send_mail(
            subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )

    def send_reservation_email(reservation, status):
        subject = f"Reserva {status}"
        message = (f"Olá {reservation.user.name},\n"
                   f"Sua reserva para a sala {reservation.room.name} foi {status.lower()}.\n")
        EmailService.send_email(subject, message, [reservation.user.email])

    # Envia e-mail ao responsável pela aprovação da reserva
    def send_responsible_email(reservation, frontend_decision_url):
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
        EmailService.send_email(subject, message, [reservation.responsible.email], html_message)
