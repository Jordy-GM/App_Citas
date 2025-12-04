from api import models
from ..models.User import UserProfile
from ..models.Citas import Citas
from ..models.Empresas import Empresas
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 
from django.db.models import Count, Q



class Clientesview(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        

        try:    
            # Obtiene el perfil del usuario autenticado
            user = request.user.userprofile
            # Verifica si el usuario tiene una empresa asociada
            empresa_user = Empresas.objects.filter(usuario=user).first()
            if empresa_user:
                # Obtiene los clientes asociados a la empresa del usuario
                clientes = Citas.objects.filter(empresa=empresa_user).values(
                    'usuario__user__username', 'usuario__user__email').annotate(
                    total_citas=Count('id'),
                    citas_pendientes=Count('id', filter=Q(estado='pendiente')),
                    citas_confirmadas=Count('id', filter=Q(estado='confirmado')),
                    citas_atendidas=Count('id', filter=Q(estado='atendido')),
                    citas_canceladas=Count('id', filter=Q(estado='cancelado'))
                    ).order_by('-total_citas')  # Ordenar por más citas primero
                    
                total = Citas.objects.filter(empresa=empresa_user).count()
                
                return Response({"clientes":list(clientes),
                                 "total_citas":total}, status=status.HTTP_200_OK)
            
        except Empresas.DoesNotExist:
            return Response({"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND)




    
