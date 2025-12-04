"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views.user_signup_views import signup_User_view
from api.views.user_login_views import UserLoginView
from api.views.citas_views import Citas_View
from api import urls 
from api.views.Atendido_views import Atendido_View
from api.views.dashboard_view import DashboardView
from api.views.clientes_view import Clientesview
#token authentication JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Importar las nuevas vistas de password reset
from api.views.Reset_view import (
    PasswordResetRequestView,
    PasswordResetVerifyTokenView,
    PasswordResetConfirmView,
    ChangePasswordView,
    LogoutAllDevicesView,
    UserProfileView
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup', signup_User_view.as_view(), name='signup'),
    path('api/login', UserLoginView.as_view(), name='login'),
    path('api/citas', Citas_View.as_view(), name='citas_get_post'),
    path('api/citas/<int:id>', Citas_View.as_view(), name='citas_update_delete'), # pach y delete citas por id
    path('api/atenciones', Atendido_View.as_view(), name='atenciones_get'),  # get citas atendidas por empresa)
    path('api/atenciones/<int:id>', Atendido_View.as_view(), name='atenciones_update'),  # patch citas atendidas por id
    
    path('api/dashboard', DashboardView.as_view(), name='dashboard'),  # get dashboard de citas y atenciones
    path('api/clientes', Clientesview.as_view(), name='clientes'),  # get clientes asociados a la empresa del usuario autenticado
    
    #token authentication JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    #reset password
    # RUTAS - Password Reset System
    path('api/password-reset/request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/password-reset/verify/', PasswordResetVerifyTokenView.as_view(), name='password_reset_verify'),
    path('api/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('api/user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('api/auth/logout-all/', LogoutAllDevicesView.as_view(), name='logout_all_devices'),
    
    
    # Documentación de API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI (interfaz interactiva)
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # ReDoc (documentación alternativa más limpia)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
     
]
