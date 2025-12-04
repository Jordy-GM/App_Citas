"""
Serializers para la documentación drf-spectacular de password reset
Estos serializers son SOLO para documentar las respuestas en Swagger
"""
from rest_framework import serializers #type: ignore


# ============================================================================
# SCHEMAS DE DATOS BÁSICOS (para reutilizar)
# ============================================================================

class UserDataSerializer(serializers.Serializer):
    """Schema para datos básicos del usuario"""
    
    id = serializers.IntegerField(
        help_text='ID del usuario'
    )
    username = serializers.CharField(
        help_text='Nombre de usuario'
    )
    email = serializers.EmailField(
        help_text='Email del usuario'
    )


class TokensSerializer(serializers.Serializer):
    """Schema para tokens JWT"""
    
    access = serializers.CharField(
        help_text='Token de acceso JWT'
    )
    refresh = serializers.CharField(
        help_text='Token de refresh JWT'
    )


# ============================================================================
# SCHEMAS DE RESPUESTAS GENERALES
# ============================================================================

class SuccessResponseSerializer(serializers.Serializer):
    """Schema para respuestas exitosas generales"""
    
    success = serializers.BooleanField(
        help_text='Indica si la operación fue exitosa'
    )
    message = serializers.CharField(
        help_text='Mensaje descriptivo'
    )
    sessions_closed = serializers.IntegerField(
        required=False,
        help_text='Número de sesiones cerradas (solo para logout all)'
    )


class ErrorResponseSerializer(serializers.Serializer):
    """Schema para respuestas de error"""
    
    success = serializers.BooleanField(
        help_text='Siempre false en errores',
        default=False
    )
    message = serializers.CharField(
        help_text='Mensaje de error'
    )
    errors = serializers.DictField(
        required=False,
        help_text='Detalles específicos de errores de validación'
    )


# ============================================================================
# SCHEMAS ESPECÍFICOS DE PASSWORD RESET
# ============================================================================

class TokenVerifyResponseSerializer(serializers.Serializer):
    """Schema para respuesta de verificación de token"""
    
    valid = serializers.BooleanField(
        help_text='Indica si el token es válido'
    )
    message = serializers.CharField(
        help_text='Mensaje descriptivo'
    )
    user = UserDataSerializer(
        required=False,
        help_text='Datos del usuario si el token es válido'
    )


class ResetConfirmResponseSerializer(serializers.Serializer):
    """Schema para respuesta de confirmación de reset"""
    
    success = serializers.BooleanField(
        help_text='Indica si la operación fue exitosa'
    )
    message = serializers.CharField(
        help_text='Mensaje descriptivo'
    )
    tokens = TokensSerializer(
        required=False,
        help_text='Nuevos tokens JWT para iniciar sesión'
    )
    user = UserDataSerializer(
        required=False,
        help_text='Datos del usuario'
    )


# ============================================================================
# SCHEMAS DE USER PROFILE
# ============================================================================

class UserProfileDataSerializer(serializers.Serializer):
    """Schema para datos completos del perfil"""
    
    id = serializers.IntegerField(
        help_text='ID del perfil'
    )
    user = UserDataSerializer(
        help_text='Datos del usuario asociado'
    )
    profile_picture = serializers.URLField(
        required=False,
        allow_null=True,
        help_text='URL de la imagen de perfil'
    )
    created_at = serializers.DateTimeField(
        help_text='Fecha de creación del perfil'
    )
    updated_at = serializers.DateTimeField(
        help_text='Última actualización del perfil'
    )


class UserProfileResponseSerializer(serializers.Serializer):
    """Schema para respuesta de perfil de usuario"""
    
    success = serializers.BooleanField(
        help_text='Indica si la operación fue exitosa'
    )
    user = UserProfileDataSerializer(
        help_text='Datos completos del perfil'
    )