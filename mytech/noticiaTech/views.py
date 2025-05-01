from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Noticia
from .serializers import NoticiasSerializer
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


#API Q BUSCA TODOS AS NOTICIAS
@api_view(['GET'])
@throttle_classes([UserRateThrottle, AnonRateThrottle]) #Tds tipos de usuarios terá limite de acesso para consumir a api externa
def Buscando_noticias(request):
    dados = Noticia.objects.all() #Dados do banco
    serializer = NoticiasSerializer(dados, many =True)
    return Response({'dadosModel':serializer.data})

    
#API QUE BUSCA POR UMA ÚNICA NOTÍCIA
@api_view(['GET'])
def detalhe_noticias(request, pk):
    dados = get_object_or_404(Noticia,id =pk)
    serializer = NoticiasSerializer(dados)
    return Response(serializer.data, status=200)







