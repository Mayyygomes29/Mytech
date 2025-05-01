from rest_framework.serializers import ModelSerializer
from .models import Perfil
class Perfil_Serializer(ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'