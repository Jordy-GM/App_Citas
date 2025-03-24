from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



# modelo de usuario personalizado que hereda de AbstractUser
# AbstractUser es un Modelo de usuario predeterminado en Django
class UserProfile (models.Model):
    
    # establece una relación uno a uno entre UserProfile y el modelo User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) 
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='image/profile.jpg')
    email = models.EmailField(max_length=50, blank=False, unique=True)
    empresa = models.CharField(max_length=100, blank=False, null=True)
    
    
    #Control de duplicados de correo y email en el modelo UserProfile
    def clean(self):
        
        error = {}
        
        if UserProfile.objects.filter(email=self.email).exists():
            error['email'] = ValidationError('Este Email ya esta en uso')
        
        if UserProfile.objects.filter(user__username=self.user.username).exists():
            error['username'] =  ValidationError('Este Usuario ya esta en uso')
      
      
      
    def __str__(self):
            return self.user.username + '|' + self.email