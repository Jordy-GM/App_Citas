from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Empresas (models.Model):
    
    nombre = models.CharField(max_length=50, blank=False, null=False, required=True)
    direccion = models.CharField(max_length=50, blank=False, null=False, uniquie=True)
    telefono = PhoneNumberField(blank=False, null=False, unique=True, region='EC')
    
    
    def __str__(self):
        return self.nombre
