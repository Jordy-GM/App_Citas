from ..models.Citas import Citas
from ..models.Empresas import Empresas
from rest_framework import status
from rest_framework.views import APIView as Apiview
from rest_framework.response import Response
from ..serializers.Citas_serializers import CitaSerializer
from ..serializers.Empresa_serializer import EmpresaSerializer
from rest_framework.permissions import IsAuthenticated
from ..models.Atenciones import Atenciones
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django.db.models.functions import TruncMonth
from django.db import models




class DashboardView(Apiview):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        
        #verificamos si el usuario tiene empresa asociada
        empresa = Empresas.objects.get(usuario = request.user.userprofile)
        if not empresa:
            return Response({"error": "No tienes una empresa asociada"}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # Obtenemos el perfil del usuario autenticado
            user_profile = request.user.userprofile
            
            # Contamos el número de citas asociadas a la empresa del usuario
            citas_number = Citas.objects.exclude(estado='atendido').filter(empresa=empresa).count()
            
            # Contamos el número de atenciones asociadas a la empresa del usuario
            atenciones_number = Citas.objects.filter(empresa=empresa, estado='atendido').count()

            # Contamos el número de citas pendientes de la empresa del usuario
            pendientes = Citas.objects.filter(empresa=empresa, estado='pendiente').count()
            
            # Contamos el número de citas canceladas de la empresa del usuario
            cancelado = Citas.objects.filter(empresa=empresa, estado ='cancelado').count()
            

           # Obtener la empresa del usuario autenticado
            empresa = Empresas.objects.get(usuario=request.user.userprofile)

            # Contamos el número de clientes únicos con citas en esta empresa
            mis_clientes = Citas.objects.filter(
                empresa=empresa).values('usuario').distinct().count()

            # Servicio más solicitado (Top 10)
            servicios_top = Citas.objects.filter(empresa=empresa)\
                .values('servicio')\
                .annotate(total=Count('servicio'))\
                .order_by('-total')[:10]

            # Citas por número de la semana (1 = domingo, 7 = sábado)

            # Consulta de citas agrupadas por día de la semana
            citas_por_dia = Citas.objects.filter(empresa=empresa)\
                .annotate(dia_semana=ExtractWeekDay('fecha'))\
                .values('dia_semana')\
                .annotate(total=Count('id'))\
                .order_by('dia_semana')

            # Citas por mes
            citas_por_mes = Citas.objects.filter(empresa=empresa)\
                .annotate(mes=TruncMonth('fecha'))\
                .values('mes')\
                .annotate(total=Count('id'))\
                .order_by('mes')

            # Porcentaje de citas por estado
            total = Citas.objects.filter(empresa=empresa).count()
            estados = Citas.objects.filter(empresa=empresa)\
                .values('estado')\
                .annotate(total=Count('id'))

            porcentaje_por_estado = [
                {"estado": e["estado"], "porcentaje": round((e["total"] / total) * 100, 2)}
                for e in estados
            ]

            # Clientes con más citas (Top 5)
            clientes_frecuentes = Citas.objects.filter(empresa=empresa)\
                .values(username=models.F('usuario__user__username'))\
                .annotate(total=Count('id'))\
                .order_by('-total')[:5]


            # Preparamos los datos para la respuesta
            data = {
                "empresa": EmpresaSerializer(empresa).data,
                "mis_clientes": mis_clientes,
                "clientes_frecuentes": list(clientes_frecuentes),
                "citas_number": citas_number,
                "citas_por_dia": list(citas_por_dia),
                "citas_por_mes": list(citas_por_mes),
                "porcentaje_por_estado": porcentaje_por_estado,
                "atenciones_number": atenciones_number,
                "pendientes": pendientes,
                "cancelado": cancelado, 
                "servicios mas solicitados": servicios_top,
                "user_profile": {
                    "username": user_profile.user.username,
                    "email": user_profile.user.email,
                    "profile_picture": user_profile.profile_picture.url if user_profile.profile_picture else None
                }
            }
            
            return Response(data, status=status.HTTP_200_OK)
        
        
        
        
        
        