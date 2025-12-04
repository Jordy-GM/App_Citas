from django.db import models
from api.models.Citas import Citas
from api.models.Empresas import Empresas

class Atenciones (models.Model):
    
    cita = models.ForeignKey(Citas, on_delete=models.CASCADE)
    fecha_atencion = models.DateField(blank=False, null=False, unique=False )
    empresas = models.ForeignKey(Empresas, on_delete=models.CASCADE, null=True)
    #notas = models.TextField(max_length=100, blank=True, null=True, unique=False)
    
    def __str__(self):        
        
        return f" Cita atendida de {self.cita.usuario.user} el {self.fecha_atencion}"
    



