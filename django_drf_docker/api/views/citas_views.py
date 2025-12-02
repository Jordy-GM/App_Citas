from api.models.Citas import Citas
from ..models.Empresas import Empresas
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.Citas_serializers import CitaSerializer
from ..serializers.Empresa_serializer import EmpresaSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.User import UserProfile
from ..models.Atenciones import Atenciones
from django.utils import timezone

class Citas_View(APIView):
    
    #el usuario cliente debe elegir la empresa a la que desea pedir la cita
    
    permission_classes = [IsAuthenticated]
    
    #funcion para guardar una cita
    def post(self, request):
        
        #1,2 obtener el perfil del usuario autenticado
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"error": "Perfil de usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        #1 extrae el valor de la clave 'empresa' del diccionario de datos de la solicitud
        empresa_id = request.data.get('empresa')
        if not empresa_id:
            return Response({'no se ha seleccionado una empresa'}, status=status.HTTP_400_BAD_REQUEST)
        
        #1Busca un único registro en la tabla Empresas donde el campo nombre coincida con el valor de empresa_id.
        try:
            empresa = Empresas.objects.get(nombre=empresa_id)
        except Empresas.DoesNotExist:
            return Response({"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        
        #2 verifica si el usuario logeado tiene relacion con una empresa
        if not Empresas.objects.filter(usuario=request.user.userprofile).exists():
            request.data['estado'] = 'pendiente'
            
        #3 define los campos y validaciones para el modelo llamado Citas
        serializer = CitaSerializer(data=request.data) 
        #3 asigna el usuario y la empresa al objeto Citas antes de guardarlo
        if serializer.is_valid():
            serializer.save(usuario=user_profile, empresa=empresa)  # ← ¡ASIGNACIÓN DIRECTA AQUÍ!
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    
    
    #funcion para listar las citas que el usuario tiene
    def get(self, request):
        
        request_username = request.user.username
        
        try:
            
        
            empresa = Empresas.objects.get(usuario=request.user.userprofile) # Obtener la empresa asociada al usuario
            #print(empresa.nombre)
            cita= Citas.objects.exclude(estado='atendido').filter(empresa=empresa) # Filtrar citas por la empresa del usuario
            serializer = CitaSerializer(cita, many=True)
            return Response({"username": request_username,
                             "citas separadas de mi empresa": serializer.data,
                             }, status=status.HTTP_200_OK)
        
        except Empresas.DoesNotExist:
            
            # Si no hay empresa asociada al usuario, devuelve las citas del usuario    
            cita = Citas.objects.filter(usuario=request.user.userprofile)
            serializer = CitaSerializer(cita, many=True)
            # Filtrar las empresas disponibles
            empresas = Empresas.objects.exclude(nombre__isnull=True).values_list('nombre', flat=True)
            return Response(
                {"citas" : serializer.data,
                "username" : request_username,
                "empresas disponibles": list(empresas)            
                }, status=status.HTTP_200_OK)
            
    def patch(self, request, id):
        
        try:
            
            empresa = Empresas.objects.get(usuario=request.user.userprofile) # Obtiene la empresa asociada al usuario autenticado
        
            # Intenta obtener la cita por su ID
            cita = Citas.objects.get(id=id, empresa=empresa)  # Asegúramos de que la cita pertenece a la empresa del usuario
            # Guarda el estado anterior de la cita
            estado_anterior = cita.estado  
            # Si la cita existe, actualiza los campos permitidos, patrial=True permite actualizar solo un campo
            serializer = CitaSerializer(cita, data=request.data, partial=True)
            if serializer.is_valid():
                cita_actualizada = serializer.save()
                
                 # Si el estado de la cita cambia a 'atendido', crea o actualiza Atenciones fecha_atencion
                if estado_anterior != 'atendido' and cita_actualizada.estado == 'atendido':
                    Atenciones.objects.update_or_create(
                        cita=cita_actualizada,
                        defaults={
                            "fecha_atencion": timezone.localdate(),  # Solo la fecha
                            'empresas': empresa  # Asigna la empresa actual
                        }
                    )
                    return Response({"message": "Cita actualizada y atención registrada",
                                     "cita": serializer.data,
                                     }, status=status.HTTP_200_OK)
                    
                elif estado_anterior == 'atendido' and cita_actualizada.estado != 'atendido':
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

    def delete(self, request, id):
        try:
        
            empresa = Empresas.objects.filter(usuario=request.user.userprofile).first()
            cita = (Citas.objects.filter(id=id, empresa=empresa) | Citas.objects.filter(id=id, usuario=request.user.userprofile)).first()
            cita.delete()
            return Response({"message": "Cita eliminada"}, status=status.HTTP_204_NO_CONTENT)

        except Empresas.DoesNotExist:
            return Response({"error": "Empresa no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        except Citas.DoesNotExist:
            return Response({"error": "Cita no encontrada"}, status=status.HTTP_404_NOT_FOUND)
