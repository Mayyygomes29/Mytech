from django.db import models


class Vagas(models.Model):
    Titulo =  models.CharField(max_length=70)
    Empresa = models.CharField(max_length=70)
    Localizacao = models.CharField(max_length=200)
    Descricao = models.TextField()
    url = models.URLField(default='None')
    
    
  
