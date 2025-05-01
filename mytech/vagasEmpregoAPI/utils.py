from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

#Filtragem 
def filtragem(request):
    return {
    'what' : request.query_params.get('what', ''),
    'ordering-crescente' : request.query_params.get('ordering-crescente'),
    'ordering-decrescente' : request.query_params.get('ordering-decrescente'), 
    'ordering-gte' : request.query_params.get('ordering-gte'),
    'ordering-lte' : request.query_params.get('ordering-lte'),
    'where' : request.query_params.get('where', '' ),
    'search': request.query_params.get('search', ''),
    'page' : request.query_params.get('page', 1),
    'perpage':request.query_params.get('perpage', 10),
    }



#Configura um throttle personalizado
class PersoThrottleParaVagas(AnonRateThrottle):
    scope = 'ten'