from rest_framework import serializers
from .models import Noticia

class NoticiasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = '__all__'