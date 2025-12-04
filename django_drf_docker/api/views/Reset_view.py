from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from ..models.User import UserProfile
from ..serializers.Reset_serializers import (
    PasswordResetRequestSerializer,
    PasswordResetVerifyTokenSerializer,
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    LogoutAllDevicesSerializer
)

from ..docs.decorators.reset_decorator import (
    password_reset_request_decorator,
    password_reset_verify_decorator,
    password_reset_confirm_decorator,
    change_password_decorator,
    user_profile_decorator,
    logout_all_devices_decorator
)

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    inline_serializer,
)


@method_decorator([csrf_exempt, never_cache], name='dispatch')
class PasswordResetRequestView(APIView):
    """
    Solicitar reset de contraseña
    POST /api/password-reset/request/
    """
    permission_classes = [AllowAny]  # Cualquiera puede acceder, incluso sin login
    
    
    @password_reset_request_decorator # decorador para la documentación
    def post(self, request):
        # Validamos los datos enviados por el usuario
        serializer = PasswordResetRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            # Si los datos son inválidos, se devuelve un error 400
            return Response({
                'success': False,
                'message': 'Datos inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Extraemos el email y la URL del frontend
        email = serializer.validated_data['email']
        frontend_url = serializer.validated_data.get('frontend_url') or request.META.get('HTTP_ORIGIN')
        
        try:
            # Buscamos el perfil del usuario según su email
            user_profile = UserProfile.objects.select_related('user').get(user__email=email)
            # Enviamos el correo con el enlace para restablecer la contraseña
            success, message = user_profile.send_password_reset_email(frontend_url)
            
            if success:
                # Si se envió el email correctamente
                return Response({
                    'success': True,
                    'message': 'Se ha enviado un email con instrucciones para restablecer tu contraseña.'
                }, status=status.HTTP_200_OK)
            else:
                # Error al enviar email
                return Response({
                    'success': False,
                    'message': 'Error al enviar el email de recuperación.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except UserProfile.DoesNotExist:
            # No revelamos si el email existe por razones de seguridad
            return Response({
                'success': True,
                'message': 'Si el email existe, recibirás instrucciones para restablecer tu contraseña.'
            }, status=status.HTTP_200_OK)

@method_decorator([csrf_exempt, never_cache], name='dispatch')
class PasswordResetVerifyTokenView(APIView):
    """
    Verificar token de reset
    POST /api/password-reset/verify/
    """
    permission_classes = [AllowAny]  # No requiere autenticación
    
    
    @password_reset_verify_decorator  # decorador para la documentación
    def post(self, request):
        serializer = PasswordResetVerifyTokenSerializer(data=request.data)
        
        if not serializer.is_valid():
            # Si no se envía un token válido
            return Response({
                'valid': False,
                'message': 'Token requerido',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Se extrae el token enviado
        token = serializer.validated_data['token']
        user_profile = UserProfile.verify_password_reset_token(token)
        
        if user_profile:
            # Si el token es válido, se devuelve la info del usuario
            return Response({
                'valid': True,
                'message': 'Token válido',
                'user': {
                    'id': user_profile.user.id,
                    'username': user_profile.user.username,
                    'email': user_profile.user.email
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'valid': False,
                'message': 'Token inválido o expirado'
            }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator([csrf_exempt, never_cache], name='dispatch')
class PasswordResetConfirmView(APIView):
    """
    Confirmar reset de contraseña
    POST /api/password-reset/confirm/
    """
    permission_classes = [AllowAny]
    
    
    @password_reset_confirm_decorator  # decorador para la documentación
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Datos inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Extraemos el token y la nueva contraseña
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        # Verificamos si el token es válido
        user_profile = UserProfile.verify_password_reset_token(token)
        
        if not user_profile:
            return Response({
                'success': False,
                'message': 'Token inválido o expirado'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Intentamos cambiar la contraseña
        success, message = user_profile.reset_password_with_token(new_password, token)
        
        if success:
            # Generamos nuevos tokens JWT para iniciar sesión
            tokens = user_profile.generate_new_jwt_tokens()
            
            return Response({
                'success': True,
                'message': message,
                'tokens': tokens,
                'user': {
                    'id': user_profile.user.id,
                    'username': user_profile.user.username,
                    'email': user_profile.user.email
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator([csrf_exempt, never_cache], name='dispatch')
class ChangePasswordView(APIView):
    """
    Cambiar contraseña (usuario autenticado)
    POST /api/password/change/
    """
    permission_classes = [IsAuthenticated]  # Solo usuarios logueados pueden acceder
    
    
    @change_password_decorator  # decorador para la documentación
    def post(self, request):
        try:
            # Obtener el perfil del usuario autenticado
            user_profile = UserProfile.objects.select_related('user').get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Perfil de usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Validamos los datos enviados (vieja y nueva contraseña)
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'user': request.user}
        )
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Datos inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        # Intentamos cambiar la contraseña
        success, message = user_profile.change_password(old_password, new_password)
        
        if success:
            tokens = user_profile.generate_new_jwt_tokens()
            
            return Response({
                'success': True,
                'message': message,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)

@method_decorator([csrf_exempt, never_cache], name='dispatch')
class UserProfileView(APIView):
    """
    Obtener perfil del usuario
    GET /api/user/profile/
    """
    permission_classes = [IsAuthenticated]
    
    
    @user_profile_decorator  # decorador para la documentación
    def get(self, request):
        try:
            user_profile = UserProfile.objects.select_related('user').get(user=request.user)
            serializer = UserProfileSerializer(user_profile)
            
            return Response({
                'success': True,
                'user': serializer.data
            }, status=status.HTTP_200_OK)
            
        except UserProfile.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Perfil de usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)


@method_decorator([csrf_exempt, never_cache], name='dispatch')
class LogoutAllDevicesView(APIView):
    """
    Cerrar sesión en todos los dispositivos
    POST /api/auth/logout-all/
    """
    permission_classes = [IsAuthenticated]
    
    
    @logout_all_devices_decorator
    def post(self, request):
        try:
            # Obtenemos todos los tokens JWT activos del usuario
            from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
            tokens = OutstandingToken.objects.filter(user=request.user)
            
            blacklisted_count = 0
            # Intentamos bloquear (invalidar) cada token
            for token in tokens:
                try:
                    token.blacklist()
                    blacklisted_count += 1
                except:
                    continue  # Si un token no se puede invalidar, seguimos con el siguiente
            
            return Response({
                'success': True,
                'message': f'Se cerraron {blacklisted_count} sesiones activas',
                'sessions_closed': blacklisted_count
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Error al cerrar sesiones'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)