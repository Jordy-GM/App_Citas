from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Empresas (models.Model):
    
    nombre = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    telefono = PhoneNumberField(blank=True, null=True, region='EC')
    usuario = models.ForeignKey('UserProfile', on_delete=models.CASCADE, blank=True, null=True) #relaciona la empresa con el usuario
    
    
    def __str__(self):
        return self.nombre 
