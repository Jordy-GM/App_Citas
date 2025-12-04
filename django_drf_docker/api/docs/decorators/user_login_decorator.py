from drf_spectacular.utils import extend_schema # type: ignore

from ..schemas.user_login_schema import (
    LoginResponseSerializer,
    
)
from ..examples.user_login_example import (
    LOGIN_REQUEST_EXAMPLE,
    LOGIN_SUCCESS_EXAMPLE,
    LOGIN_INVALID_CREDENTIALS_EXAMPLE,
    LOGIN_PROFILE_NOT_FOUND_EXAMPLE,
    LOGIN_VALIDATION_ERROR_EXAMPLE,
)
from api.serializers.User_login_serializers import UserProfileLoginSerializer


login_docs = extend_schema(
    summary="Iniciar sesión",
    description="""
    Autentica un usuario con sus credenciales y retorna tokens JWT.
    
    **Flujo de autenticación:**
    1. Envía username y password
    2. Si las credenciales son válidas, recibe tokens de acceso y refresh
    3. Usa el token de acceso en el header: `Authorization: Bearer <access_token>`
    4. Cuando expire, usa el refresh token para obtener uno nuevo
    
    **Duración de tokens:**
    - Access token: 15 minutos (por defecto)
    - Refresh token: 7 días (por defecto)
    """,
    tags=['Autenticación'],
    request=UserProfileLoginSerializer,
    responses={
        200: LoginResponseSerializer,

    },
    examples=[
        LOGIN_REQUEST_EXAMPLE,
        LOGIN_SUCCESS_EXAMPLE,
        LOGIN_INVALID_CREDENTIALS_EXAMPLE,
        LOGIN_PROFILE_NOT_FOUND_EXAMPLE,
        LOGIN_VALIDATION_ERROR_EXAMPLE,
    ],
)