from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from api.models.User import UserProfile

class UserProfileLoginSerializer(serializers.ModelSerializer):
    
    # password solo sera de escritura y no se mostrara en la respuesta
    password = serializers.CharField(write_only=True, required=True) 
    username = serializers.CharField(required=True)
    
    class Meta:
        model = UserProfile
        fields = ['username', 'password']

    #funcion que valida el login del usuario    
    def validate_login(self, data): #funcion que recibe los datos del cliente en data 
        if data.get('password') and data.get('username'):   # si data contiene diccionario password y username con sus valores
            
            user = authenticate(username=data['username'], password=data['password'])  #user = authenticate(username="jordi", password="1234")
            if user:
                try:
                    user_profile = UserProfile.objects.get(user=user) # busca en la base de datos el perfil del usuario relacionado con el campo user del modelo UserProfile
                    data['user'] = user # agrega o actualiza una clave llamada 'user' dentro del diccionario data, y le asigna el valor de user.
                    data['user_profile'] = user_profile
                    return data
                except UserProfile.DoesNotExist:
                    raise serializers.ValidationError('User profile does not exist')
            else:
                raise serializers.ValidationError('Invalid credentials')
        return data
