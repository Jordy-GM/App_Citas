from rest_framework import serializers
from api.models.Empresas import Empresas

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresas
        fields = ['nombre','direccion','telefono']
        
    extra_kwargs = {
        'nombre': {'required': False},
        'direccion':{'required': False}, 
        'telefono':{'required': False}
        
    }
    
    pass