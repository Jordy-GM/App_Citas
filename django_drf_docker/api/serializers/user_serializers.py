from rest_framework import serializers
from django.contrib.auth.models import User
from api.models.User import UserProfile



        
    
class UserProfileSerializer(serializers.ModelSerializer):
    # password solo sera de escritura y no se mostrara en la respuesta
    password = serializers.CharField(write_only=True, required=True) 
    username = serializers.CharField(required=True)

    
    class Meta:
        model = UserProfile
        fields = ['username', 'profile_picture', 'email', 'password']
        
        
        
    def create(self, validated_data):
        #Extraemos los campos adicionales del perfil
        profile_picture = validated_data.pop('profile_picture')
        
        #creamos usuario con el modelo User de Django Y el metodo create_user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
           
        )
        
        #Creamos el perfil con el modelo UserProfile
        UserProfile.objects.create(user=user, profile_picture=profile_picture,  )
        
        return user
        

    