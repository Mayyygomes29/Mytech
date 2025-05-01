from django.contrib.auth.models import User
from django.db import models


class Perfil(models.Model):
    tipo_usuario = [
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=11)
    tipo = models.CharField(max_length=25, choices=tipo_usuario)

    def __str__(self):
        return f'{self.user.username}, {self.user.first_name}, {self.user.last_name}, {self.tipo}'

# Create your models here.
