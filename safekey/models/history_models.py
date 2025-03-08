from django.db import models
from safekey.models.user_models import User
from safekey.models.room_models import Room

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Chave estrangeira para o usuário
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # Chave estrangeira para a sala
    real_date_schedulling = models.DateField(blank = False, null = False) # Campo para armazenar a data da reserva
    real_start_time = models.TimeField(blank = False, null = False) # Campo para armazenar o horário de inicio
    real_end_time = models.TimeField(blank = False, null = False) # Campo para armazenar o horário de fim
    reason = models.TextField(blank = False, null = False, max_length = 200) # campo para armazenar razao da reserva (TextField utilizado para textos grandes)
    commentary = models.TextField(max_length = 200, blank = True)  # campo para armazenar comentario da reserva 

    def __str__(self):
        return f"Reserva {self.id} - {self.user.name} - {self.room.name} - {self.real_date_schedulling} ({self.real_start_time}-{self.real_end_time})"