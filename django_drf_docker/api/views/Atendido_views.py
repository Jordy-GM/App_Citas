from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.Atenciones import Atenciones
from ..models.Citas import Citas
from ..models.Empresas import Empresas
from ..serializers.Citas_serializers import CitaSerializer
from ..serializers.Atenciones_serializers import AtencionesSerializer
from django.utils import timezone


#esta vista permite a los usuarios autenticados con empresas ver las citas que han sido atendidas
class Atendido_View(APIView):
    permission_classes = [IsAuthenticated]
    
    def get (self, request):
        
        try:
            username = request.user.username
            # get the profile of user 
            user = request.user.userprofile 
            # whit the user filter the company for the user
            empresa = Empresas.objects.filter(usuario=user).first()
            # filter the citas that have been attended
            citas = Citas.objects.filter(empresa=empresa, estado='atendido')
            if citas.exists():
                serializer = CitaSerializer(citas, many=True)
                return Response({"username": username, "citas": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No hay citas atendidas para tu susario"}, status=status.HTTP_404_NOT_FOUND)
            
        except Empresas.DoesNotExist:
                return Response({"error": "Perfil de usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            
            
    def patch(self, request, id):

        try:

            # Obtiene la empresa asociada al usuario autenticado
            empresa = Empresas.objects.get(usuario=request.user.userprofile)

            # Intenta obtener la cita por su ID
            # Asegúramos de que la cita pertenece a la empresa del usuario
            cita = Citas.objects.get(id=id, empresa=empresa)
            # Guarda el estado anterior de la cita
            estado_anterior = cita.estado
            # Si la cita existe, actualiza los campos permitidos, patrial=True permite actualizar solo un campo
            serializer = CitaSerializer(cita, data=request.data, partial=True)
            if serializer.is_valid():
                cita_actualizada = serializer.save()
                
                # Si el estado de la cita cambia de 'atendido' a  cualquier otro estado, elimina de Atenciones 
                if estado_anterior == 'atendido' and cita_actualizada.estado != 'atendido':
                    # Si el estado cambia de 'atendido' a otro estado, elimina la atención asociada
                    Atenciones.objects.filter(cita=cita_actualizada).delete()
                    return Response({"message": "Cita actualizada y atención eliminada",
                                     "cita": serializer.data,
                                     }, status=status.HTTP_200_OK)

                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Empresas.DoesNotExist:
            return Response({"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        except Citas.DoesNotExist:
            return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)
