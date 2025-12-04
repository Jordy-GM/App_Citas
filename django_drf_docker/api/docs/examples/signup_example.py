from drf_spectacular.utils import OpenApiExample # type: ignore


# Ejemplo de request para registro de usuario completo
registration_request_example = OpenApiExample(
    name='Registro de usuario completo',
    summary='Ejemplo de registro con todos los campos',
    description='Muestra cómo registrar un usuario con información completa incluyendo datos de empresa',
    value={
        "username": "juan_perez",
        "email": "juan.perez@ejemplo.com",
        "password": "MiPassword123!",
        "profile_picture": None,
        "empresa": {
            "nombre": "Tech Solutions SA",
            "direccion": "Av. Principal 123, Guayaquil",
            "telefono": "+593987654321"
        }
    },
    request_only=True
)


# Ejemplo de request mínimo (sin empresa)
registration_request_minimal_example = OpenApiExample(
    name='Registro mínimo',
    summary='Ejemplo con campos requeridos solamente',
    description='Registro con los campos mínimos obligatorios (sin empresa)',
    value={
        "username": "maria_gomez",
        "email": "maria.gomez@ejemplo.com",
        "password": "Password456!"
    },
    request_only=True
)


# Ejemplo de respuesta exitosa de registro
registration_success_example = OpenApiExample(
    name='Registro exitoso',
    summary='Usuario creado correctamente',
    description='Respuesta cuando el usuario se registra exitosamente',
    value={
        "message": "User created successfully",
        "username": "juan_perez",
        "email": "juan.perez@ejemplo.com"
    },
    response_only=True,
    status_codes=['201']
)


# Ejemplo de respuesta con errores de validación
registration_error_example = OpenApiExample(
    name='Errores de validación',
    summary='Datos inválidos en el registro',
    description='Respuesta cuando hay errores en los datos enviados',
    value={
        "username": [
            "A user with that username already exists."
        ],
        "email": [
            "Enter a valid email address."
        ],
        "password": [
            "This password is too short. It must contain at least 8 characters."
        ]
    },
    response_only=True,
    status_codes=['400']
)


# Ejemplo alternativo de error - campos faltantes
registration_error_missing_fields_example = OpenApiExample(
    name='Campos requeridos faltantes',
    summary='Faltan campos obligatorios',
    description='Error cuando no se envían todos los campos requeridos',
    value={
        "username": [
            "This field is required."
        ],
        "email": [
            "This field is required."
        ],
        "password": [
            "This field is required."
        ]
    },
    response_only=True,
    status_codes=['400']
)


# Ejemplo alternativo de error - error creando empresa
registration_error_empresa_invalid_example = OpenApiExample(
    name='Error al crear empresa',
    summary='Error en los datos de la empresa',
    description='Error cuando hay problemas al crear la empresa asociada',
    value={
        "empresa": [
            "Error creating empresa: Invalid data provided"
        ]
    },
    response_only=True,
    status_codes=['400']
)


# Ejemplo de lista de empresas disponibles
empresas_list_example = OpenApiExample(
    name='Lista de empresas',
    summary='Empresas disponibles para registro',
    description='Lista completa de empresas disponibles en el sistema',
    value={
        "empresas disponibles": [
            "Tech Solutions SA",
            "Innovatech Corp",
            "Digital Services Ltd",
            "Sistemas Integrados CIA",
            "Consultora Empresarial"
        ]
    },
    response_only=True,
    status_codes=['200']
)


# Ejemplo de lista vacía de empresas (edge case)
empresas_list_empty_example = OpenApiExample(
    name='Sin empresas disponibles',
    summary='No hay empresas registradas',
    description='Caso cuando no existen empresas en el sistema',
    value={
        "empresas disponibles": []
    },
    response_only=True,
    status_codes=['200']
)


# Ejemplo de error interno del servidor
internal_error_example = OpenApiExample(
    name='Error del servidor',
    summary='Error interno (500)',
    description='Error inesperado en el servidor',
    value={
        "error": "Internal server error. Please try again later."
    },
    response_only=True,
    status_codes=['500']
)