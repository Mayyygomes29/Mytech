from django.urls import path

from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('lista-vagas/', views.ListarVagas, name='Api de lista de vagas'),
    path('lista-vagas/<int:pk>', views.DetalhesVaga.as_view(), name ='Detalhes da vaga de emprego'),
]
