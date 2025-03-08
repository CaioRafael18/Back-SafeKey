from django.db import models

class UserType(models.Model):
    type = models.CharField(max_length = 20, blank = False, null = False, unique = True) # tipo do usuário

    def __str__(self):
        return self.type