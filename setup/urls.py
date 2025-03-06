from django.contrib import admin
from django.urls import path, include
from safekey.views.authentication_views import loginView
from safekey.views.history_views import HistoryViewSet
from safekey.views.reservation_views import ReservationViewSet
from safekey.views.room_views import RoomViewSet
from safekey.views.user_views import UserViewSet
from safekey.views.user_types_views import UsersTypesViewSet
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

# Roteador para as rotas
router = routers.DefaultRouter()
router.register('users', UserViewSet) # Registrando minha rota do UsuarioViewSet
router.register('usersTypes', UsersTypesViewSet) # Registrando minha rota do UsuarioViewSet
router.register('rooms', RoomViewSet) # Registrando minha rota do RoomViewSet
router.register('reservations', ReservationViewSet) # Registrando minha rota do ReservationViewSet
router.register('history', HistoryViewSet, basename='history') # Registrando minha rota do HistoryViewSet

# Rotas adicionais para as ações customizadas (approve e reject)
reservation_router = router.urls
reservation_approve_reject_urls = [
    path('reservations/<int:pk>/approve/', ReservationViewSet.as_view({'get': 'approve'}), name='approve-reservation'),
    path('reservations/<int:pk>/reject/', ReservationViewSet.as_view({'get': 'reject'}), name='reject-reservation'),
]

urlpatterns = [
   path('admin/', admin.site.urls),
   path('', include(router.urls)),
   path('login/', loginView.as_view(), name='login'),
   path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   *reservation_approve_reject_urls,
]
