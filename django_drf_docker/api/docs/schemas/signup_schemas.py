from rest_framework import serializers # type: ignore


class EmpresaRequestSerializer(serializers.Serializer):
    """Schema para los datos de empresa en el registro"""
    
    nombre = serializers.CharField(
        max_length=255,
        required=True,
        help_text='Nombre de la empresa'
    )
    direccion = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        help_text='Dirección de la empresa'
    )
    telefono = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True,
        help_text='Teléfono de contacto de la empresa'
    )


class UserRegistrationRequestSerializer(serializers.Serializer):
    """Schema para el request de registro de usuario"""
    
    username = serializers.CharField(
        max_length=150,
        min_length=3,
        required=True,
        help_text='Nombre de usuario único'
    )
    email = serializers.EmailField(
        required=True,
        help_text='Correo electrónico del usuario'
    )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        help_text='Contraseña del usuario (mínimo 8 caracteres)'
    )
    profile_picture = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text='Imagen de perfil del usuario (opcional)'
    )
    empresa = EmpresaRequestSerializer(
        required=False,
        allow_null=True,
        help_text='Datos de la empresa asociada al usuario (opcional)'
    )


class UserRegistrationResponseSerializer(serializers.Serializer):
    """Schema para la respuesta exitosa de registro"""
    
    message = serializers.CharField(
        help_text='Mensaje de confirmación'
    )
    username = serializers.CharField(
        help_text='Nombre de usuario registrado'
    )
    email = serializers.EmailField(
        help_text='Email del usuario registrado'
    )


class EmpresasListResponseSerializer(serializers.Serializer):
    """Schema para la lista de empresas disponibles"""
    
    empresas_disponibles = serializers.ListField(
        child=serializers.CharField(),
        help_text='Lista de nombres de empresas disponibles'
    )


class ErrorResponseSerializer(serializers.Serializer):
    """Schema para respuestas de error"""
    
    error = serializers.CharField(
        required=False,
        help_text='Mensaje de error general'
    )
    username = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='Errores relacionados con el campo username'
    )
    email = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='Errores relacionados con el campo email'
    )
    password = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='Errores relacionados con el campo password'
    )
    empresa = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='Errores relacionados con el campo empresa'
    )
    profile_picture = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='Errores relacionados con el campo profile_picture'
    )


class UserRegistrationResponseSerializer(serializers.Serializer):
    """Schema para la respuesta exitosa de registro"""
    
    message = serializers.CharField(
        help_text='Mensaje de confirmación'
    )
    username = serializers.CharField(
        help_text='Nombre de usuario registrado'
    )
    email = serializers.EmailField(
        help_text='Email del usuario registrado'
    )


class EmpresasListResponseSerializer(serializers.Serializer):
    """Schema para la lista de empresas disponibles"""
    
    empresas_disponibles = serializers.ListField(
        child=serializers.CharField(),
        help_text='Lista de nombres de empresas disponibles'
    )


class ErrorDetailSerializer(serializers.Serializer):
    """Schema para detalles de error de un campo específico"""
    
    field_errors = serializers.ListField(
        child=serializers.CharField(),
        help_text='Lista de mensajes de error para un campo'
    )


class ErrorResponseSerializer(serializers.Serializer):
    """Schema para respuestas de error"""
    
    error = serializers.CharField(
        required=False,
        help_text='Mensaje de error general'
    )
    username = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='Errores relacionados con el campo username'
    )
    email = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='Errores relacionados con el campo email'
    )
    password = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='Errores relacionados con el campo password'
    )
    empresa = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='Errores relacionados con el campo empresa'
    )