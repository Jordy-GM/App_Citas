from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from ..models.User import UserProfile

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializador para manejar solicitudes de restablecimiento de contraseña.
    Valida y procesa el correo electrónico para el restablecimiento.
    """
    email = serializers.EmailField(
        required=True,
        help_text="Correo electrónico del usuario que solicita el restablecimiento de contraseña"
    )
    
    frontend_url = serializers.URLField(
        required=False,
        help_text="URL del frontend para construir el enlace de restablecimiento",
        allow_blank=True
    )
    
    def validate_email(self, value):
        """Normaliza el correo convirtiéndolo a minúsculas y eliminando espacios en blanco"""
        return value.lower().strip()


class PasswordResetVerifyTokenSerializer(serializers.Serializer):
    """
    Serializador para verificar tokens de restablecimiento de contraseña.
    Valida el token JWT proporcionado para el restablecimiento.
    """
    token = serializers.CharField(
        required=True,
        help_text="Token JWT de restablecimiento de contraseña"
    )
    
    def validate_token(self, value):
        """Valida que el token no esté vacío"""
        if not value.strip():
            raise serializers.ValidationError("Token inválido")
        return value.strip()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializador para confirmar el restablecimiento de contraseña.
    Maneja la validación del token y la confirmación de la nueva contraseña.
    """
    token = serializers.CharField(required=True)
    
    new_password = serializers.CharField(
        required=True,
        min_length=8,  # Longitud mínima de la contraseña
        max_length=128,  # Longitud máxima de la contraseña
        style={'input_type': 'password'}  # Se muestra como campo tipo contraseña
    )
    
    confirm_password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=128,
        style={'input_type': 'password'}
    )
    
    def validate_token(self, value):
        """Valida el token de restablecimiento y verifica si ha expirado"""
        if not value.strip():
            raise serializers.ValidationError("Token inválido")
        
        # Verifica el token usando el método del modelo UserProfile
        user_profile = UserProfile.verify_password_reset_token(value.strip())
        if not user_profile:
            raise serializers.ValidationError("Token inválido o expirado")
        
        return value.strip()
    
    def validate_new_password(self, value):
        """Valida que la nueva contraseña cumpla con los requisitos de seguridad"""
        try:
            # Crea un usuario temporal para validar la contraseña con los validadores de Django
            temp_user = User(username='temp', email='temp@temp.com')
            validate_password(value, temp_user)
        except ValidationError as e:
            # Convierte el ValidationError de Django a ValidationError de DRF
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, data):
        """Validación cruzada de campos para asegurar que las contraseñas coincidan"""
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise serializers.ValidationError({
                    'confirm_password': 'Las contraseñas no coinciden'
                })
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializador para cambiar la contraseña (usuarios autenticados).
    Requiere la contraseña actual y valida la nueva contraseña.
    """
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}  # Se muestra como campo tipo contraseña
    )
    
    new_password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=128,
        style={'input_type': 'password'}
    )
    
    confirm_password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=128,
        style={'input_type': 'password'}
    )
    
    def validate_new_password(self, value):
        """Valida que la nueva contraseña cumpla con los requisitos de seguridad"""
        user = self.context.get('user')  # Obtiene el usuario desde el contexto
        try:
            validate_password(value, user)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value
    
    def validate(self, data):
        """Validación cruzada de campos para cambio de contraseña"""
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        old_password = data.get('old_password')
        
        # Verifica si las nuevas contraseñas coinciden
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise serializers.ValidationError({
                    'confirm_password': 'Las contraseñas no coinciden'
                })
        
        # Verifica si la nueva contraseña es distinta a la actual
        if old_password and new_password:
            if old_password == new_password:
                raise serializers.ValidationError({
                    'new_password': 'La nueva contraseña debe ser diferente a la actual'
                })
        
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar la información del perfil del usuario.
    Incluye campos relacionados del modelo User en formato de solo lectura.
    """
    # Todos estos campos provienen del modelo relacionado User
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'username',         # Desde el modelo User
            'email',            # Desde el modelo User
            'first_name',       # Desde el modelo User
            'last_name',        # Desde el modelo User
            'profile_picture',  # Desde el modelo UserProfile
            'date_joined'       # Desde el modelo User
        ]


class LogoutAllDevicesSerializer(serializers.Serializer):
    """
    Serializador para cerrar sesión en todos los dispositivos.
    Campo de confirmación simple para evitar uso accidental.
    """
    confirm = serializers.BooleanField(
        required=False,
        default=True,
        help_text="Campo de confirmación para cerrar sesión en todos los dispositivos"
    )
