from django.urls import path
from .views import RegistrarUser, CustomTokenObtainPairView, CustomTokenRefreshView
from rest_framework_simplejwt.views import  TokenBlacklistView


urlpatterns = [
    path('register-user/', RegistrarUser.as_view(), name='Cadastrando usuario'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='Gera um token de acesso, caso o user for autenticado. E salva no cookie httpsonly'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='Gera um token refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token vai p/ lista negra qnd o usuario faz logout' )


]
