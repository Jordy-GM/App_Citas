from rest_framework import serializers
from api.models.Citas import Citas
from ..models.Empresas import Empresas
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CitaSerializer(serializers.ModelSerializer):
    #nombre de la empresa
    empresa = serializers.CharField(source='empresa.nombre', read_only=True)
    
    class Meta():
        model = Citas
        fields = ['id','fecha', 'descripcion', 'servicio', 'estado', 'notas', 'empresa']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'datetime-local'}),  # Cambia el tipo de campo a datetime-local
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Cambia el tipo de campo a textarea
            'servicio': forms.Select(choices=[
                ('consulta', 'Consulta'),
                ('corte_de_pelo', 'Corte de pelo'),
                ('otro', 'Otro')
            ]),
            
        }
    
    

    
