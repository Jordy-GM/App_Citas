from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from api.models.User import UserProfile
from api.models.Empresas import Empresas
from api.serializers.Empresa_serializer import EmpresaSerializer


        
    
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True) #campo opcional para la imagen de perfil
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)     # password solo sera de escritura y no se mostrara en la respuesta 
    empresa = EmpresaSerializer(required=False) #campo opcional para la empresa


        
    class Meta:
        model = User
        fields = ['username', 'profile_picture', 'email', 'password', 'empresa']
        
        
    
    def create(self, validated_data):
        #Extraemos los campos adicionales del perfil
        profile_picture = validated_data.pop('profile_picture', None)
        # Extraemos los datos de empresa si existen
        empresa_data = validated_data.pop('empresa', None)
        
        #creamos usuario con el modelo User de Django Y el metodo create_user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        
        #Creamos el perfil con el modelo UserProfile
        user_profile = UserProfile.objects.create(user=user, profile_picture=profile_picture)
        
            # Crear Empresa si hay datos
        if empresa_data:
            try: empresa = Empresas.objects.create(
                nombre=empresa_data.get('nombre'),
                direccion=empresa_data.get('direccion'),
                telefono=empresa_data.get('telefono'),
                usuario=user_profile  # Asignar el UserProfile, no el User
            )
            except Exception as e:
                raise serializers.ValidationError(f"Error creating empresa: {str(e)}")
        
        # Guardamos el usuario en la base de datos
        return user
    
    
