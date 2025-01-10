from django.contrib import admin
from django.urls import path, include
from safekey.views import UsuarioViewSet, TiposUsuariosView, loginView
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView

schema_view = get_schema_view(
   openapi.Info(
      title="Documentação da API",
      default_version='v1',
      description="Documentação da API SafeKey",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

router = routers.DefaultRouter()
router.register('usuarios', UsuarioViewSet) # Registrando minha rota do UsuarioViewSet
router.register('tiposUsuarios', TiposUsuariosView) # Registrando minha rota do UsuarioViewSet

urlpatterns = [
   path('admin/', admin.site.urls),
   path('', include(router.urls)),
   path('login/', loginView.as_view(), name='login'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
