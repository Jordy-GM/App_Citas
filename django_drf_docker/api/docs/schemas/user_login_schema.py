from rest_framework import serializers # type: ignore
from drf_spectacular.utils import ( # type: ignore
    extend_schema_view,
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    inline_serializer,
)


# ========== SCHEMAS ==========

# Serializer para la respuesta exitosa de login
class LoginResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Token de refresco JWT")
    access = serializers.CharField(help_text="Token de acceso JWT")
    user_id = serializers.IntegerField(help_text="ID del usuario")
    username = serializers.CharField(help_text="Nombre de usuario")
    email = serializers.EmailField(help_text="Email del usuario")