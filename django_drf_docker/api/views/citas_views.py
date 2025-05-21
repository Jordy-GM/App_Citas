from api.models.Citas import Citas
from ..models.Empresas import Empresas
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.Citas_serializers import CitaSerializer
from ..serializers.Empresa_serializer import EmpresaSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.User import UserProfile


class Citas_View(APIView):
    
    #el usuario cliente debe elegir la empresa a la que desea pedir la cita
    
    permission_classes = [IsAuthenticated]
    
    #funcion para guardar una cita
    def post(self, request):
        
        #obtener el perfil del usuario autenticado
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"error": "Perfil de usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        #validar que haya una empresa seleccionada
        empresa_id = request.data.get('empresa')
        if not empresa_id:
            return Response({'no se ha seleccionado una empresa'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            empresa = Empresas.objects.get(nombre=empresa_id)
        
        serializer = CitaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=user_profile, empresa=empresa)  # ← ¡ASIGNACIÓN DIRECTA AQUÍ!
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    #funcion para listar las citas que el usuario tiene
    def get(self, request):
        request_id = request.user.id
        request_username = request.user.username
        citas = Citas.objects.filter(usuario=request_id)
        serializer = CitaSerializer(citas, many=True)
        # Filtrar las empresas disponibles
        empresas = Empresas.objects.exclude(nombre__isnull=True).values_list('nombre', flat=True)
        return Response(
            {"citas" : serializer.data,
            "username" : request_username,
            "empresas disponibles": list(empresas)            
            }, status=status.HTTP_200_OK)
    
