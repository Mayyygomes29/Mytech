from django.contrib import admin
from .models import Vagas

@admin.register(Vagas)
class VagasAdmin(admin.ModelAdmin):
    list_display = ('Titulo', 'Empresa', 'Localizacao', 'url')
    search_fields = ['Titulo']


# Register your models here.
