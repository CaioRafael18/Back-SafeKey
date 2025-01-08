from django.db import models

class Usuario(models.Model):
    # Como será salvo no banco e como será exibido
    tipos = (
            ('Administrador', 'Administrador'),
            ('Professor', 'Professor') ,
            ('Aluno', 'Aluno')
            )
    nome = models.CharField(max_length = 100, blank = False, unique = True) # Tamanho 100, não pode estar em branco e valor unico
    email = models.EmailField(max_length = 40, blank = False, unique = True) # Tamanho 100, não pode estar em branco e valor unico
    senha = models.CharField(max_length = 128, blank = False) # Tamanho 100 e não pode estar em branco
    tipo = models.CharField(max_length = 13, choices = tipos, blank = False, default = 'Aluno') # Tamanho 13(maior escolha), deverá escolher um dos tipos, não pode estar branco e nem nulo, tendo aluno como padrão

    def __str__(self):
        return self.nome
    
class TipoUsuario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE) # se um usuario for deletado, seu TipoUsuario correspondente também será excluído.

    def __str__(self):
        return f"{self.usuario.nome} ({self.usuario.id})" 
