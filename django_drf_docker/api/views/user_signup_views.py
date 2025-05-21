from ..serializers.User_signup_serializers import UserProfileSerializer 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.Empresas import Empresas
from ..serializers.Empresa_serializer import EmpresaSerializer

#se crea la vista para el registro de usuarios con la clase personaliable APIView de Django Rest Framework


class signup_User_view(APIView):
    
    #funcion para listar las empresas disponibles
    def get(self, request):
        nombres = Empresas.objects.exclude(nombre__isnull=True).values_list('nombre', flat=True)
        return Response({'empresas disponibles': list(nombres)})
       

    def post(self, request):
        
        #request.data contiene los datos enviados por el usuario en el cuerpo del request (como en un formulario POST) Y si todo está bien: crea el objeto User en la base de datos.
        serializer = UserProfileSerializer(data=request.data) 
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'username': user.username,
                'email': user.email,
            }, status=status.HTTP_201_CREATED

            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
