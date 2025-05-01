from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import generics
from .utils import filtragem
from rest_framework.permissions import AllowAny
from .models import Vagas
from .serializers import VagasSerializer
from .paginations import CustomPagination
from mytech.servicers.api_emprego import ApiEmprego
from django.core.cache import cache



#Lista todas as vagas
@api_view(['GET'])
@permission_classes([AllowAny])
def ListarVagas(request):
    vagas_cache = cache.get('vagas')

    if vagas_cache:
        vagas = Vagas.objects.filter(id__in=vagas_cache)
    else:
        api = ApiEmprego()
        response = api.get(request)

        if 'vagas' in response.data:
            for vaga_data in response.data['vagas']:
                vaga = Vagas(**vaga_data)  
                vaga.save()
            vagas = Vagas.objects.all()
            cache.set("vagas", list(vagas.values_list('id', flat=True)), timeout=86400)
        else:
            vagas = Vagas.objects.all()

    filter = filtragem(request)

    if filter["what"]:
        vagas = vagas.filter(Titulo__icontains=filter["what"])
    if filter["ordering-crescente"]:
        vagas = vagas.order_by(filter["ordering-crescente"])
    if filter["ordering-decrescente"]:
        vagas = vagas.order_by(f'-{filter["ordering-decrescente"]}')
    if filter['ordering-gte']:
        vagas = vagas.filter(id__gte=filter['ordering-gte'])
    if filter['ordering-lte']:
        vagas = vagas.filter(id__lte=filter['ordering-lte'])
    if filter['search']:
        vagas = vagas.filter(Q(Titulo__icontains=filter['search']) | Q(Empresa__icontains=filter['search']))

    if vagas.exists():
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(vagas, request)
        serializer = VagasSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    return Response({'message': 'Não existe vagas'}, status=404)



#Busca por uma única vaga especifica
class DetalhesVaga(generics.RetrieveAPIView):
    queryset = Vagas.objects.all()
    serializer_class = VagasSerializer









