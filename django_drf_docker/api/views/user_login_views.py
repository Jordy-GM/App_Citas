from ..serializers.User_login_serializers import UserProfileLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from api.models.User import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken


class UserLoginView(APIView):
    
    def post(self, request):
        
        serializer =UserProfileLoginSerializer(data=request.data) #se crea el serializador con los datos del request
        
        if serializer.is_valid(): #si el serializador es valido
            
            #Extrae el nombre de usuario y contraseña validados.
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
            
            
        
