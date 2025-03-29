from django.db import models
from api.models.Citas import Citas

class Atenciones (models.Model):
    
    cita = models.ForeignKey(Citas, on_delete=models.CASCADE)
    fecha_atnecion = models.DateField(blank=False, null=False, unique=True )
    notas = models.TextField(max_length=100, blank=True, null=True, unique=False)
    
    def __str__(self):        
        
        return f" Cita atendida de {self.cita.usuario_id.user} el {self.fecha_atnecion}"
    
 