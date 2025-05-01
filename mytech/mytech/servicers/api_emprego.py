from django.core.cache import cache
from django.conf import settings
import requests
from vagasEmpregoAPI.models import Vagas
from vagasEmpregoAPI.utils import filtragem
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

#Api que pega a vaga de emprego e salva no banco de dados
class ApiEmprego(APIView):
    @method_decorator(cache_page(60*60))
    def get(self, request):
        
        filtros = filtragem(request) # Recupera os parâmetros da requisição
        #endpoint da API Adzuna
        endpoint = f"{settings.ADZUNA_API_BASE_URL}/{settings.ADZUNA_COUNTRY_CODE}/search/{filtros['page']}/"

        params = {
            'app_id': settings.ADZUNA_APP_ID,
            'app_key': settings.ADZUNA_APP_KEY,
            'what': filtros['what'],
            'where': filtros['where'],
        }
        headers = {
            'Content-Type': 'application/json'
        }
        vagas_salvas = []

        try:
            response = requests.get(endpoint, params=params, headers=headers)
            response.raise_for_status()  # Levanta erro se a requisição falhar
            vagas_data = response.json()  # Converte a resposta para JSON
            print("Resposta da API:", vagas_data)  # Adicione isso para verificar a resposta

            # Verifica se 'results' existe e tem vagas
            if 'results' in vagas_data:
                for vaga in vagas_data['results']:
                    empresa_nome = vaga.get('company', {}).get('display_name', 'Desconhecida')

                    # Cria uma nova vaga no banco se não existir
                    if not Vagas.objects.filter(url=vaga['redirect_url']).exists():
                        vaga_obj = Vagas.objects.create(
                            Titulo=vaga['title'],
                            Empresa=empresa_nome,
                            Descricao=vaga['description'],
                            url=vaga['redirect_url']
                        )
                        vagas_salvas.append(vaga_obj.Titulo)

                return Response({"message": "Vagas salvas com sucesso!", "vagas": vagas_salvas}, status=200)

            return Response({"message": "Nenhuma vaga encontrada."}, status=404)

        except requests.RequestException as e:
            print("Erro ao conectar com a API:", e)  # Adicione isso para verificar o erro de conexão
            return Response({"error": "Erro ao conectar com a Adzuna API", "details": str(e)}, status=503)