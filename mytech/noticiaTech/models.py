from django.db import models

class Noticia(models.Model):
    titulo = models.CharField(max_length=150)
    subtitulo = models.CharField(max_length=200)
    data = models.DateTimeField()
    conteudo = models.TextField()
    autor = models.CharField(max_length=50)
    fonte = models.CharField(max_length=255, null=True, blank=True)



    def __str__(self):
        return f'{self.titulo}, {self.subtitulo},{self.autor}'

