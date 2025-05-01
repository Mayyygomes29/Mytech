from django.contrib import admin
from .models import Noticia


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data')
    search_fields = ('titulo', 'autor')
    date_hierarchy = 'data'
# Register your models here.
