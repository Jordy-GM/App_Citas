from drf_spectacular.utils import OpenApiExample # type: ignore


LOGIN_REQUEST_EXAMPLE = OpenApiExample(
    name='Ejemplo de login',
    description='Credenciales de ejemplo para iniciar sesión',
    value={
        'username': 'juan_perez',
        'password': 'MiPassword123'
    },
    request_only=True,
)

LOGIN_SUCCESS_EXAMPLE = OpenApiExample(
    name='Login exitoso',
    description='Respuesta cuando las credenciales son correctas',
    value={
        'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
        'access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
        'user_id': 1,
        'username': 'juan_perez',
        'email': 'juan@email.com'
    },
    response_only=True,
    status_codes=['200'],
)

LOGIN_INVALID_CREDENTIALS_EXAMPLE = OpenApiExample(
    name='Credenciales inválidas',
    description='Respuesta cuando el usuario o contraseña son incorrectos',
    value={
        'error': 'Credenciales inválidas'
    },
    response_only=True,
    status_codes=['401'],
)

LOGIN_PROFILE_NOT_FOUND_EXAMPLE = OpenApiExample(
    name='Perfil no encontrado',
    description='Cuando el usuario existe pero no tiene perfil',
    value={
        'error': 'No existe un perfil para este usuario'
    },
    response_only=True,
    status_codes=['404'],
)

LOGIN_VALIDATION_ERROR_EXAMPLE = OpenApiExample(
    name='Error de validación',
    description='Cuando faltan campos obligatorios',
    value={
        'username': ['Este campo es requerido.'],
        'password': ['Este campo es requerido.']
    },
    response_only=True,
    status_codes=['400'],
)