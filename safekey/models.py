from django.db import models

class TipoUsuario(models.Model):
    tipo = models.CharField(max_length = 20, blank = False, null = False, unique = True)

    def __str__(self):
        return self.tipo

class Usuario(models.Model):
    nome = models.CharField(max_length = 100, blank = False, unique = True) # Tamanho 100, não pode estar em branco e valor unico
    email = models.EmailField(max_length = 40, blank = False, unique = True) 
    senha = models.CharField(max_length = 128, blank = False) 
    tipo = models.ForeignKey(TipoUsuario, on_delete = models.CASCADE) # Se o tipo for excluido, o usuário com esse tipo também será

    def __str__(self):
        return self.nome