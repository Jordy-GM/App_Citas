from drf_spectacular.utils import extend_schema, OpenApiResponse # type: ignore

from ...serializers.User_signup_serializers import ( UserProfileSerializer )

from ..schemas.signup_schemas import (
    EmpresasListResponseSerializer,
    ErrorResponseSerializer,)

from ..examples.signup_example import (
    registration_request_example,
    registration_request_minimal_example,
    registration_success_example,
    registration_error_example,
    registration_error_missing_fields_example,
    registration_error_empresa_invalid_example,
    empresas_list_example,
    empresas_list_empty_example
)


# Decorador para el método GET (listar empresas)
signup_get_decorator = extend_schema(
    operation_id='list_empresas_disponibles',
    summary='Listar empresas disponibles',
    description='Obtiene la lista de empresas disponibles para el registro de usuarios',
    tags=['Autenticación'],
    responses={
        200: OpenApiResponse(
            response=EmpresasListResponseSerializer,
            description='Lista de empresas disponibles'
        ),
        500: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Error interno del servidor'
        )
    },
    examples=[
        empresas_list_example,
        empresas_list_empty_example
    ]
)


# Decorador para el método POST (registro de usuario)
signup_post_decorator = extend_schema(
    operation_id='register_user',
    summary='Registrar nuevo usuario',
    description='Registra un nuevo usuario en el sistema con sus datos personales y empresa asociada',
    tags=['Autenticación'],
    request=UserProfileSerializer,
    responses={
        201: OpenApiResponse(
            response=UserProfileSerializer,
            description='Usuario creado exitosamente'
        ),
        400: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Datos inválidos o error de validación'
        ),
        500: OpenApiResponse(
            response=ErrorResponseSerializer,
            description='Error interno del servidor'
        )
    },
    examples=[
        registration_request_example,
        registration_request_minimal_example,
        registration_success_example,
        registration_error_example,
        registration_error_missing_fields_example,
        registration_error_empresa_invalid_example
    ]
)