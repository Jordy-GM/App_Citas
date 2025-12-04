from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
import secrets
from datetime import datetime, timedelta
import jwt


# modelo de usuario personalizado que hereda de User
# User es un Modelo de usuario predeterminado en Django
class UserProfile (models.Model):
    
    # establece una relación uno a uno entre UserProfile y el modelo User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) 
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='image/profile.jpg')
    #campos para resetablecer la contraseña
    reset_token = models.CharField(max_length=512, blank=True, null=True)  # Token para restablecer la contraseña
    reset_token_created = models.DateTimeField(blank=True, null=True)  # Fecha de creación del token
    
    
    #Control de duplicados de correo y email en el modelo UserProfile
    def clean(self):
        
        error = {}
        
        if UserProfile.objects.filter(email=self.email).exists():
            error['email'] = ValidationError('Este Email ya esta en uso')
        
        if UserProfile.objects.filter(user__username=self.user.username).exists():
            error['username'] =  ValidationError('Este Usuario ya esta en uso')
            
    def __str__(self):
            return self.user.username + '|' + self.user.email
        
        
        
    ###############################################-Metodos para restablecer la contraseña-####################################################
    
    def generate_password_reset_token(self):
        """
        Genera un token JWT específicamente para la funcionalidad de restablecimiento de contraseña.
        Compatible con la librería Simple JWT.
        """
        # Crea el contenido del token con información del usuario y metadatos
        payload = {
            'user_id': self.user.id,            # ID del usuario para identificación
            'email': self.user.email,           # Email del usuario para verificación
            'username': self.user.username,     # Nombre de usuario como referencia
            'type': 'password_reset',           # Tipo de token
            'exp': timezone.now() + timedelta(hours=1),  # Expira en 1 hora
            'iat': timezone.now(),           # Fecha de emisión
        }
        
        # Codifica el contenido en un token JWT usando la SECRET_KEY de Django
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        
        # Guarda el token en el modelo para rastrear el estado
        self.reset_token = token
        self.reset_token_created = timezone.now()
        # Guarda solo los campos necesarios para eficiencia
        self.save(update_fields=['reset_token', 'reset_token_created'])
        
        return token  # Retorna el token generado


    @staticmethod
    def verify_password_reset_token(token):
        """
        Verifica y decodifica un token de restablecimiento de contraseña.
        Retorna el UserProfile si es válido, None si es inválido o ha expirado.
        """
        try:
            # Decodifica el token usando la SECRET_KEY de Django
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            # Verifica que sea un token de tipo restablecimiento
            if payload.get('type') != 'password_reset':
                return None

            # Obtiene el usuario de la base de datos usando el ID del token
            user_id = payload.get('user_id')
            # Optimiza la consulta uniendo el modelo User
            user_profile = UserProfile.objects.select_related('user').get(user__id=user_id)

            return user_profile  # Retorna el perfil del usuario

        except jwt.ExpiredSignatureError:  # El token ha expirado
            return None
        except jwt.InvalidTokenError:      # Token inválido o mal formado
            return None
        except UserProfile.DoesNotExist:   # El usuario no existe
            return None
        except Exception:                  # Cualquier otro error inesperado
            return None


    def send_password_reset_email(self, frontend_url=None):
        """
        Envía un correo de restablecimiento de contraseña que contiene un token JWT.
        """
        # Genera primero el token
        token = self.generate_password_reset_token()
        
        # Determina la URL del frontend donde se manejará el restablecimiento
        if not frontend_url:
            # Usa la URL configurada o una por defecto
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://192.168.100.10:8000')
        
        # Crea el enlace de restablecimiento con el token como parámetro
        reset_url = f"{frontend_url}/reset-password?token={token}"
        
        # Prepara el contexto para la plantilla del correo
        context = {
            'user': self.user,                           # Objeto usuario
            'reset_url': reset_url,                      # Enlace completo
            'token': token,                              # Token JWT
            'expiry_hours': 1,                           # Tiempo de validez
            'site_name': getattr(settings, 'SITE_NAME', 'Tu Aplicación'),  # Nombre del sitio
        }
        
        try:
            # Renderiza la plantilla HTML del correo con el contexto
            html_message = render_to_string('emails/password_reset.html', context)
            # Crea una versión en texto plano quitando las etiquetas HTML
            plain_message = strip_tags(html_message)
            
            # Asunto del correo
            subject = f'Restablecer contraseña - {context["site_name"]}'
            
            # Envía el correo usando la función de Django
            send_mail(
                subject,                       # Asunto
                plain_message,                 # Contenido plano
                settings.DEFAULT_FROM_EMAIL,   # Dirección del remitente
                [self.user.email],             # Destinatario (correo del usuario)
                html_message=html_message,     # Contenido HTML
                fail_silently=False,           # Lanzar excepción si falla
            )
            return True, "Email enviado exitosamente"  # Respuesta exitosa
            
        except Exception as e:
            import traceback
            traceback.print_exc()  # imprime el error completo en consola
            print(f"[ERROR] Email no enviado: {e}")
            return False, "Error al enviar el email de recuperación."


    def reset_password_with_token(self, new_password, token):
        """
        Restablece la contraseña usando un token JWT válido.
        """
        # Verifica que el token es válido y pertenece a este usuario
        user_profile = self.verify_password_reset_token(token)
        
        # Si no es válido o no pertenece al usuario actual
        if not user_profile or user_profile.user.id != self.user.id:
            return False, "Token inválido o expirado"
        
        try:
            # Establece la nueva contraseña con el método de Django
            self.user.set_password(new_password)
            # Guarda solo el campo de contraseña
            self.user.save(update_fields=['password'])
            
            # Limpia el token ya usado
            self.reset_token = None
            self.reset_token_created = None
            # Guarda solo esos campos
            self.save(update_fields=['reset_token', 'reset_token_created'])
            
            # Invalida los tokens anteriores
            self._invalidate_user_tokens()
            
            return True, "Contraseña restablecida exitosamente"
            
        except Exception as e:
            # Devuelve mensaje de error si algo falla
            return False, f"Error al restablecer contraseña: {str(e)}"


    def change_password(self, old_password, new_password):
        """
        Cambia la contraseña tras verificar la actual.
        Para usuarios autenticados.
        """
        # Verifica si la contraseña actual es correcta
        if not self.user.check_password(old_password):
            return False, "La contraseña actual es incorrecta"
        
        try:
            # Establece la nueva contraseña
            self.user.set_password(new_password)
            # Guarda solo el campo de contraseña
            self.user.save(update_fields=['password'])
            
            # Invalida tokens existentes
            self._invalidate_user_tokens()
            
            return True, "Contraseña cambiada exitosamente"
            
        except Exception as e:
            # Devuelve mensaje de error si algo falla
            return False, f"Error al cambiar contraseña: {str(e)}"


    def _invalidate_user_tokens(self):
        """
        Método privado para invalidar todos los tokens JWT del usuario.
        Usa el sistema de blacklist de SimpleJWT si está disponible.
        """
        try:
            # Importa solo cuando se necesite
            from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
            # Obtiene todos los tokens activos del usuario
            tokens = OutstandingToken.objects.filter(user=self.user)
            # Los añade a la blacklist uno por uno
            for token_obj in tokens:
                try:
                    token_obj.blacklist()
                except:
                    continue  # Si falla uno, continúa
        except ImportError:
            # Si no está instalada la blacklist, no hacer nada
            pass
        except Exception:
            # Fallo silencioso para no interrumpir el proceso
            pass


    def generate_new_jwt_tokens(self):
        """
        Genera nuevos tokens JWT tras cambiar la contraseña.
        Devuelve el token de acceso y el de refresco.
        """
        # Importación bajo demanda
        from rest_framework_simplejwt.tokens import RefreshToken
        
        # Genera los tokens para el usuario
        refresh = RefreshToken.for_user(self.user)
        return {
            'refresh': str(refresh),               # Token de refresco
            'access': str(refresh.access_token),   # Token de acceso
        }


    def get_active_sessions_count(self):
        """
        Obtiene la cantidad de sesiones activas o tokens válidos del usuario.
        """
        try:
            # Importa solo si es necesario
            from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
            # Retorna la cantidad de tokens activos
            return OutstandingToken.objects.filter(user=self.user).count()
        except:
            return  # Si falla, retorna None
