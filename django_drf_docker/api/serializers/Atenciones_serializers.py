from rest_framework import serializers
from ..models import Atenciones


class AtencionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atenciones
        fields = ['fecha_atnecion', 'notas']
        
    