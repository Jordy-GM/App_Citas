from django.db import models
from api.models.User import UserProfile
from api.models.Empresas import Empresas

class Citas(models.Model):
    
    usuario_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, null=False)
    fecha = models.DateTimeField(blank=False, null=True, )
    descripcion = models.TextField(max_length=50, blank=False, null=False)
    
    
    
    def __str__(self):
        return f"Cita de {self.usuario_id} en {self.empresa.nombre} el {self.fecha}"
    
