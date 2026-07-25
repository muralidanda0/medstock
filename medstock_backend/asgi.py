import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medstock_backend.settings')

# get_asgi_application() must be called BEFORE importing anything that
# touches Django models (like our routing/consumers) — otherwise Django
# apps aren't loaded yet and you'll get cryptic import errors.
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import realtime.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(realtime.routing.websocket_urlpatterns)
    ),
})