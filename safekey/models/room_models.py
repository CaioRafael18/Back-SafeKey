from django.db import models

class Room(models.Model):
    STATUS_KEY_CHOICES = [
        ('Disponivel', 'Disponivel'),
        ('Retirada', 'Retirada')
    ]

    STATUS_CHOICES_ROOM = [
        ('Disponivel','Disponivel'),
        ('Reservada','Reservada'),
        ('Ocupado','Ocupado'),
    ]

    name = models.CharField(max_length = 30, blank = False, unique = True) # nome da sala
    block = models.CharField(max_length = 10, blank = False) # bloco da sala
    floor = models.CharField(max_length = 10, blank = False) # andar da sala
    type  = models.CharField(max_length = 15, blank = False) # tipo da sala
    status = models.CharField(max_length = 20, choices=STATUS_CHOICES_ROOM, default = 'Disponivel', editable=False) # status da sala (editable Impede edição no formulário)
    status_key = models.CharField(max_length = 20, choices=STATUS_KEY_CHOICES, default = "Disponivel", editable=False) # status da chave da sala 

    def __str__(self):
        return self.name
