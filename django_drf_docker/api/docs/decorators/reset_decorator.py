"""
Decoradores drf-spectacular para endpoints de gestión de contraseñas
"""
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ...serializers.Reset_serializers import (
    PasswordResetRequestSerializer,
    PasswordResetVerifyTokenSerializer,
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    LogoutAllDevicesSerializer
)
from ..schemas.reset_schema import (
    SuccessResponseSerializer,
    ErrorResponseSerializer,
    TokenVerifyResponseSerializer,
    ResetConfirmResponseSerializer,
    UserProfileResponseSerializer
)
from ..examples.reset_example import (
    # Request examples
    password_reset_request_example,
    verify_token_request_example,
    reset_confirm_request_example,
    change_password_request_example,
    logout_all_request_example,
    # Response examples
    reset_request_success_example,
    reset_request_error_example,
    verify_token_success_example,
    verify_token_invalid_example,
    reset_confirm_success_example,
    reset_confirm_error_example,
    change_password_success_example,
    change_password_error_example,
    user_profile_success_example,
    user_profile_not_found_example,
    logout_all_success_example,
    logout_all_error_example
)


# Decorador para solicitar reset de contraseña
password_reset_request_decorator = extend_schema(
    operation_id='password_reset_request',
    summary='Solicitar reset de contraseña',
    description='Envía un email con un token para restablecer la contraseña del usuario',
    tags=['Autenticación - Password Reset'],
    request=PasswordResetRequestSerializer,
    responses={
        200: OpenApiResponse(
            response=SuccessResponseSerializer,
            description='Email enviado exitosamente'
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Datos inválidos'
        ),
        500: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Error al enviar email'
        )
    },
    examples=[
        password_reset_request_example,
        reset_request_success_example,
        reset_request_error_example
    ]
)


# Decorador para verificar token
password_reset_verify_decorator = extend_schema(
    operation_id='password_reset_verify_token',
    summary='Verificar token de reset',
    description='Verifica si el token de reset de contraseña es válido y no ha expirado',
    tags=['Autenticación - Password Reset'],
    request=PasswordResetVerifyTokenSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenVerifyResponseSerializer,
            description='Token válido'
        ),
        400: OpenApiResponse(
            response=TokenVerifyResponseSerializer,
            description='Token inválido o expirado'
        )
    },
    examples=[
        verify_token_request_example,
        verify_token_success_example,
        verify_token_invalid_example
    ]
)


# Decorador para confirmar reset
password_reset_confirm_decorator = extend_schema(
    operation_id='password_reset_confirm',
    summary='Confirmar reset de contraseña',
    description='Restablece la contraseña usando el token válido y retorna nuevos tokens JWT',
    tags=['Autenticación - Password Reset'],
    request=PasswordResetConfirmSerializer,
    responses={
        200: OpenApiResponse(
            response=ResetConfirmResponseSerializer,
            description='Contraseña restablecida exitosamente'
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Token inválido o contraseña débil'
        )
    },
    examples=[
        reset_confirm_request_example,
        reset_confirm_success_example,
        reset_confirm_error_example
    ]
)


# Decorador para cambiar contraseña (usuario autenticado)
change_password_decorator = extend_schema(
    operation_id='change_password',
    summary='Cambiar contraseña',
    description='Permite al usuario autenticado cambiar su contraseña proporcionando la actual',
    tags=['Autenticación - Gestión de Cuenta'],
    request=ChangePasswordSerializer,
    responses={
        200: OpenApiResponse(
            response=ResetConfirmResponseSerializer,
            description='Contraseña cambiada exitosamente'
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Contraseña actual incorrecta o nueva contraseña inválida'
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='No autenticado'
        ),
        404: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Perfil no encontrado'
        )
    },
    examples=[
        change_password_request_example,
        change_password_success_example,
        change_password_error_example
    ]
)


# Decorador para obtener perfil
user_profile_decorator = extend_schema(
    operation_id='get_user_profile',
    summary='Obtener perfil del usuario',
    description='Retorna la información del perfil del usuario autenticado',
    tags=['Autenticación - Gestión de Cuenta'],
    responses={
        200: OpenApiResponse(
            response=UserProfileResponseSerializer,
            description='Perfil obtenido exitosamente'
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='No autenticado'
        ),
        404: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Perfil no encontrado'
        )
    },
    examples=[
        user_profile_success_example,
        user_profile_not_found_example
    ]
)


# Decorador para cerrar sesión en todos los dispositivos
logout_all_devices_decorator = extend_schema(
    operation_id='logout_all_devices',
    summary='Cerrar sesión en todos los dispositivos',
    description='Invalida todos los tokens JWT activos del usuario, cerrando sesión en todos los dispositivos',
    tags=['Autenticación - Gestión de Cuenta'],
    request=LogoutAllDevicesSerializer,
    responses={
        200: OpenApiResponse(
            response=SuccessResponseSerializer,
            description='Sesiones cerradas exitosamente'
        ),
        401: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='No autenticado'
        ),
        500: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Error al cerrar sesiones'
        )
    },
    examples=[
        logout_all_request_example,
        logout_all_success_example,
        logout_all_error_example
    ]
)