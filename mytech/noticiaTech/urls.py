from django.urls import path
from . import views

urlpatterns = [
    path('noticias/', views.Buscando_noticias, name= 'api de noticias' ),
    path('detalhe-noticia/<int:pk>', views.detalhe_noticias, name='detalhes noticias' )
    
]
