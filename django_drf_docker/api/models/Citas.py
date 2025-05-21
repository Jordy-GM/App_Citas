from django.db import models
from api.models.User import UserProfile
from api.models.Empresas import Empresas

class Citas(models.Model):
    
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False)
    empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, null=True)
    fecha = models.DateTimeField(blank=False, null=True, )
    descripcion = models.TextField(max_length=50, blank=False, null=False)
    servicio = models.CharField(max_length=50, blank=False, null=False) # Qué servicio va a recibir (consulta, corte de pelo, etc.).
    estado = models.CharField(max_length=50, blank=False, null=False) #pendiente, confirmado, cancelado, etc.
    notas = models.TextField(max_length=50, blank=True, null=False) #	Notas adicionales (ej: "Traer receta médica").
    
    
    def __str__(self):
        return f"Cita de {self.usuario} en {self.empresa.nombre} el {self.fecha}"
    
