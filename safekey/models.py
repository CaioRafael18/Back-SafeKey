from django.db import models
from django.utils.timezone import now

class UserType(models.Model):
    type = models.CharField(max_length = 20, blank = False, null = False, unique = True) # tipo do usuário

    def __str__(self):
        return self.type

class User(models.Model):
    name = models.CharField(max_length = 100, blank = False, unique = True) # campo para armazenar o nome do usuário (Tamanho 100, não pode estar em branco e valor unico)
    email = models.EmailField(max_length = 40, blank = False, unique = True) # campo para armazenar o email do usuário
    password = models.CharField(max_length = 128, blank = False) # campo para armazenar a senha do usuário
    type = models.ForeignKey(UserType, on_delete=models.CASCADE) # campo para armenar o tipo do usuário (Se o tipo for excluido, o usuário com esse tipo também será)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    name = models.CharField(max_length = 30, blank = False, unique = True) # nome da sala
    block = models.CharField(max_length = 10, blank = False, unique = True) # bloco da sala
    floor = models.CharField(max_length = 10, blank = False, unique = True) # andar da sala
    type  = models.CharField(max_length = 15, blank = False, unique = True) # tipo da sala
    status = models.CharField(max_length = 20, blank = False, unique = True, default = 'Disponivel', editable=False) # status da sala (editable Impede edição no formulário)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Chave estrangeira para o usuário
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # Chave estrangeira para a sala
    date = models.DateField(blank = False, null = False, unique = True) # Campo para armazenar a data da reserva
    start_time = models.TimeField(blank = False, null = False, unique = True) # Campo para armazenar o horário de inicio
    end_time = models.TimeField(blank = False, null = False, unique = True) # Campo para armazenar o horário de fim
    reason = models.TextField(blank = False, null = False, max_length = 200) # campo para armazenar razao da reserva (TextField utilizado para textos grandes)
    commentary = models.TextField(max_length = 200, blank = True)  # campo para armazenar comentario da reserva 
    deleted_at = models.DateTimeField(null = True, blank = True, editable=False) # Campo para gerenciar a exclusão do registro

    # Exclui o registro
    def delete(self):
        self.deleted_at = now()
        self.save()

    # Restaura o registro excluido
    def restore(self):
        self.deleted_at = None
        self.save()
