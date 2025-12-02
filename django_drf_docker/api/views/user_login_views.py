from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers.User_login_serializers import UserProfileLoginSerializer
from api.models.User import UserProfile

#swagger documentation decorator
from ..docs.decorators.user_login_decorator import login_docs
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    inline_serializer,
)

# Serializer para la respuesta exitosa de login
class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Token de refresco JWT")
    access = serializers.CharField(help_text="Token de acceso JWT")
    user_id = serializers.IntegerField(help_text="ID del usuario")
    username = serializers.CharField(help_text="Nombre de usuario")
    email = serializers.EmailField(help_text="Email del usuario")


class UserLoginView(APIView):
    """
    Vista para autenticación de usuarios.
    Permite iniciar sesión y obtener tokens JWT.
    """
    
    @login_docs
    def post(self, request):
        """
        Endpoint para iniciar sesión.
        
        Recibe username y password, valida las credenciales
        y retorna tokens JWT si son correctas.
        """
        serializer = UserProfileLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                
                try:
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user_id': user.id,
                        'username': user.username,
                        'email': user.email,
                    }, status=status.HTTP_200_OK)
                    
                except UserProfile.DoesNotExist:
                    return Response({
                        'error': 'No existe un perfil para este usuario'
                    }, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    'error': 'Credenciales inválidas'
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
