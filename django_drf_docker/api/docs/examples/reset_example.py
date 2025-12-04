"""
Ejemplos para la documentación drf-spectacular de password reset
"""
from drf_spectacular.utils import OpenApiExample # type: ignore


# ============================================================================
# REQUEST EXAMPLES
# ============================================================================

password_reset_request_example = OpenApiExample(
    name='Solicitar reset de contraseña',
    summary='Request para solicitar reset',
    description='Envía email de recuperación al usuario',
    value={
        "email": "usuario@ejemplo.com",
    },
    request_only=True
)

verify_token_request_example = OpenApiExample(
    name='Verificar token',
    summary='Request para verificar token',
    description='Verifica si el token es válido',
    value={
        "token": "abc123def456ghi789jkl012mno345pqr678"
    },
    request_only=True
)

reset_confirm_request_example = OpenApiExample(
    name='Confirmar reset',
    summary='Request para confirmar reset',
    description='Establece nueva contraseña con token válido',
    value={
        "token": "abc123def456ghi789jkl012mno345pqr678",
        "new_password": "NuevaPassword123!",
        "confirm_password": "NuevaPassword123!"
    },
    request_only=True
)

change_password_request_example = OpenApiExample(
    name='Cambiar contraseña',
    summary='Request para cambiar contraseña',
    description='Usuario autenticado cambia su contraseña',
    value={
        "old_password": "PasswordActual123!",
        "new_password": "NuevaPassword456!",
        "confirm_password": "NuevaPassword456!"
    },
    request_only=True
)

logout_all_request_example = OpenApiExample(
    name='Cerrar todas las sesiones',
    summary='Request para logout all',
    description='Body vacío, solo requiere autenticación',
    value={},
    request_only=True
)


# ============================================================================
# RESPONSE EXAMPLES - PASSWORD RESET REQUEST
# ============================================================================

reset_request_success_example = OpenApiExample(
    name='Email enviado exitosamente',
    summary='Reset solicitado correctamente',
    description='Se envió el email de recuperación',
    value={
        "success": True,
        "message": "Se ha enviado un email con instrucciones para restablecer tu contraseña."
    },
    response_only=True,
    status_codes=['200']
)

reset_request_error_example = OpenApiExample(
    name='Email inválido',
    summary='Error en los datos enviados',
    description='El email no es válido',
    value={
        "success": False,
        "message": "Datos inválidos",
        "errors": {
            "email": ["Enter a valid email address."]
        }
    },
    response_only=True,
    status_codes=['400']
)


# ============================================================================
# RESPONSE EXAMPLES - VERIFY TOKEN
# ============================================================================

verify_token_success_example = OpenApiExample(
    name='Token válido',
    summary='Token verificado exitosamente',
    description='El token es válido y no ha expirado',
    value={
        "valid": True,
        "message": "Token válido",
        "user": {
            "id": 1,
            "username": "juan_perez",
            "email": "juan.perez@ejemplo.com"
        }
    },
    response_only=True,
    status_codes=['200']
)

verify_token_invalid_example = OpenApiExample(
    name='Token inválido',
    summary='Token no válido o expirado',
    description='El token no existe o ya expiró',
    value={
        "valid": False,
        "message": "Token inválido o expirado"
    },
    response_only=True,
    status_codes=['400']
)


# ============================================================================
# RESPONSE EXAMPLES - RESET CONFIRM
# ============================================================================

reset_confirm_success_example = OpenApiExample(
    name='Reset exitoso',
    summary='Contraseña restablecida',
    description='La contraseña se cambió y se generaron nuevos tokens',
    value={
        "success": True,
        "message": "Contraseña restablecida exitosamente",
        "tokens": {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
        },
        "user": {
            "id": 1,
            "username": "juan_perez",
            "email": "juan.perez@ejemplo.com"
        }
    },
    response_only=True,
    status_codes=['200']
)

reset_confirm_error_example = OpenApiExample(
    name='Error al restablecer',
    summary='Token inválido o contraseña débil',
    description='No se pudo restablecer la contraseña',
    value={
        "success": False,
        "message": "Token inválido o expirado"
    },
    response_only=True,
    status_codes=['400']
)


# ============================================================================
# RESPONSE EXAMPLES - CHANGE PASSWORD
# ============================================================================

change_password_success_example = OpenApiExample(
    name='Cambio exitoso',
    summary='Contraseña cambiada',
    description='Se cambió la contraseña y se generaron nuevos tokens',
    value={
        "success": True,
        "message": "Contraseña cambiada exitosamente",
        "tokens": {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
        }
    },
    response_only=True,
    status_codes=['200']
)

change_password_error_example = OpenApiExample(
    name='Error al cambiar',
    summary='Contraseña actual incorrecta',
    description='La contraseña actual no coincide',
    value={
        "success": False,
        "message": "La contraseña actual es incorrecta"
    },
    response_only=True,
    status_codes=['400']
)


# ============================================================================
# RESPONSE EXAMPLES - USER PROFILE
# ============================================================================

user_profile_success_example = OpenApiExample(
    name='Perfil obtenido',
    summary='Datos del perfil',
    description='Información completa del perfil del usuario',
    value={
        "success": True,
        "user": {
            "id": 1,
            "user": {
                "id": 5,
                "username": "juan_perez",
                "email": "juan.perez@ejemplo.com"
            },
            "profile_picture": "https://ejemplo.com/media/profiles/juan.jpg",
            "created_at": "2025-01-15T10:30:00Z",
            "updated_at": "2025-11-27T15:45:00Z"
        }
    },
    response_only=True,
    status_codes=['200']
)

user_profile_not_found_example = OpenApiExample(
    name='Perfil no encontrado',
    summary='Error 404',
    description='El perfil del usuario no existe',
    value={
        "success": False,
        "message": "Perfil de usuario no encontrado"
    },
    response_only=True,
    status_codes=['404']
)


# ============================================================================
# RESPONSE EXAMPLES - LOGOUT ALL DEVICES
# ============================================================================

logout_all_success_example = OpenApiExample(
    name='Sesiones cerradas',
    summary='Logout exitoso',
    description='Se cerraron todas las sesiones activas',
    value={
        "success": True,
        "message": "Se cerraron 3 sesiones activas",
        "sessions_closed": 3
    },
    response_only=True,
    status_codes=['200']
)

logout_all_error_example = OpenApiExample(
    name='Error al cerrar sesiones',
    summary='Error en logout',
    description='Ocurrió un error al cerrar las sesiones',
    value={
        "success": False,
        "message": "Error al cerrar sesiones"
    },
    response_only=True,
    status_codes=['500']
)