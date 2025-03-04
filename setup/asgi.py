import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from safekey.consumers import RoomStatusConsumer  
from django.urls import path
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler  # Importa o handler de arquivos estáticos

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": ASGIStaticFilesHandler(get_asgi_application()), # Lida com requisições HTTP normais
    "websocket": AuthMiddlewareStack(  # Lida com conexões WebSocket
        URLRouter([
            path("ws/status/", RoomStatusConsumer.as_asgi()),
        ])
    ),
})