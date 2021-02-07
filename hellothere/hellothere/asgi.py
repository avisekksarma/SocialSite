"""
ASGI config for hellothere project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hellothere.settings')

import chat.routing

# ProtocolTypeRouter does the job of knowing websocket or http based on protocol i.e. ws:// or http:// and forwards to 'http' or 'websocket' key of the dictionary
# In other words: ProtocolTypeRouter Takes a mapping of protocol type names to other Application instances,
# and dispatches to the right one based on protocol name (or raises an error)
application = ProtocolTypeRouter(
    {
        # if http request sent by browser/user then the 
        # request may be is forwarded to projects' urls.py then from there to respective
        # app's urls.py then to the view function which returns the httpresponse to the browser.
        'http':get_asgi_application(),
        'websocket':AuthMiddlewareStack(
            SessionMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        ))
    }
)
