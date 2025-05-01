from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.exceptions import AuthenticationFailed

#Registra o usuario 
class RegistrarUser(APIView):
    permission_classes = [AllowAny] #Nao precisa de autenticação nesta view
    def post(self, request):
        
        #Pega os dados pela url
        username=request.data.get('username')
        password=request.data.get('password')
        test_password = request.data.get('test_password')
        cpf=request.data.get('cpf')
        telefone=request.data.get('telefone')
        tipo=request.data.get('tipo')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')

        #Se password for igual test_password é pq as senhas são parecidas, então faça:
        if password == test_password:     
            if not User.objects.filter(username=username).exists():  #Se usuário não existir, vai criar um usuario
               #Cria um usuario user
                try:
                    user = User.objects.create_user(
                        username=username,
                        password=password, 
                        email=email, 
                        first_name=first_name, 
                        last_name=last_name
                        )
                    #Continua criando o user, com acréscimo de dados necessários passado no DB
                    Perfil =Perfil.objects.create(
                        user= user, 
                        cpf=cpf, 
                        telefone=telefone, 
                        tipo=tipo
                        )
        

                    return Response({'message': 'Usuário criado com sucesso.'}, status=201)
                except Exception as e:
                    print(f"Erro inesperado ao salvar usuário: {e}")

            else:
                return Response({'message': 'Usuário já existe!'}, status=400)
        else:
            return Response({'message':'As senhas não são compatíveis.'}, status=400)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception= True)
        tokens = serializer.validated_data

        access_token = tokens.get('access')
        refresh_token = tokens.get('refresh')

        response = Response({'message':'Login com sucesso!'})

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite=None
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite=None
        )
        return response

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
       refresh_token = request.COOKIES.get('refresh_token')

       if refresh_token is None:
            raise AuthenticationFailed('Refresh token não encontrado no cookie.')

        # Tenta gerar novo access_token
       serializer = self.get_serializer(data={'refresh': refresh_token})
       serializer.is_valid(raise_exception=True)

       access_token = serializer.validated_data.get('access')

       response = Response({'Message': 'Novo Access_token gerado com sucesso!'})

        #Atualiza o cookie com o novo access token
       response.set_cookie(
            key='access_token',
            value= access_token,
            httponly= True,
            secure= False,
            samesite=None
        )
       return response

#Quando o usuário fizer o logout, o token sera colocado no blacklist, mesmo se o tempo nao tiver sido expirado
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh = request.data('refresh')
            token = RefreshToken(refresh)
            token.blacklist()
            return Response(status=205)
        except Exception:
            return Response(status=400)
