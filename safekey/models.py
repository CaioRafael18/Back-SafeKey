from django.db import models
from django.core.exceptions import ValidationError
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
    block = models.CharField(max_length = 10, blank = False) # bloco da sala
    floor = models.CharField(max_length = 10, blank = False) # andar da sala
    type  = models.CharField(max_length = 15, blank = False) # tipo da sala
    status = models.CharField(max_length = 20, blank = False, default = 'Disponivel', editable=False) # status da sala (editable Impede edição no formulário)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Aprovado', 'Aprovado'),
        ('Recusado', 'Recusado')
    ]
    APPROVERS = ['Professor', 'Administrador']

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations') # Chave estrangeira para o usuário
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'type__type__in': APPROVERS}, related_name='responsible_reservations', null = True) # Chave estrangeira para o usuário responsável pela autorização da reserva(sendo apenas prof ou admin)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) # Chave estrangeira para a sala
    date_schedulling = models.DateField(blank = False, null = False) # Campo para armazenar a data da reserva
    start_time = models.TimeField(blank = False, null = False) # Campo para armazenar o horário de inicio
    end_time = models.TimeField(blank = False, null = False) # Campo para armazenar o horário de fim
    reason = models.TextField(blank = False, null = False, max_length = 200) # campo para armazenar razao da reserva (TextField utilizado para textos grandes)
    commentary = models.TextField(max_length = 200, blank = True)  # campo para armazenar comentario da reserva 
    status = models.CharField(max_length = 20, choices=STATUS_CHOICES, default='Aprovado', editable=False) # campo para armazenar o status da reserva
    deleted_at = models.DateTimeField(null = True, blank = True, editable=False) # Campo para gerenciar a exclusão do registro

    # Exclui o registro
    def delete(self):
        self.insert_history()
        self.deleted_at = now()
        self.save()

    def insert_history(self):
        # Cria na tabela historico o registro da reserva que será deletado ao ser entregue a chave
        History.objects.create(
            user=self.user,
            room=self.room,
            real_date_schedulling=self.date_schedulling,
            real_start_time=self.start_time,
            real_end_time=self.end_time,
            reason=self.reason,
            commentary=self.commentary
        )
        
    def check_reservation(self):
        # Verifica se há conflito de reservas para a mesma sala e horário
        conflict = Reservation.objects.filter(
            room=self.room,
            date_schedulling=self.date_schedulling,
            deleted_at__isnull=True,
            start_time__lt=self.end_time, # lt: menor que 
            end_time__gt=self.start_time # gt: maior que 
        ).exclude(id=self.id)  # Exclui a própria reserva se for uma edição para não ter risco de comparar com ela mesma

        if conflict.exists():
            raise ValidationError({'detail': "A sala já está reservada para o mesmo dia e horário."})

    def clean(self):
        # Executa validação ao tentar salvar, clean é um metodo padrão utilizado para validações
        self.check_reservation()
        if self.user.type.type == 'Aluno':
            self.status = 'Pendente'

    def save(self, *args, **kwargs):
        if not self.pk:
            #Sobrescreve save() para sempre chamar clean() antes de salvar, save é um metodo padrão utilizado antes de salvar no banco
            self.clean()              
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva {self.id} - {self.room.name} - {self.date_schedulling} ({self.start_time}-{self.end_time})"
    
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
