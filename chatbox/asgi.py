"""
ASGI config for chatbox project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

'''import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbox.settings')

application = get_asgi_application()'''


from email.mime import application
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chatapp.consumers import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbox.settings')

application = get_asgi_application()

ws_patterns = [
    path('ws/chat/', )
]

application = ProtocolTypeRouter({
    'websocket' : URLRouter(ws_patterns)
})