from rest_framework import serializers
from .models import Vagas

class VagasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vagas
        fields = "__all__"