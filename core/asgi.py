import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_asgi_application()


# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# import app.routers
# import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             app.routers.websocket_urlpatterns
#         )
#     ),
# })
