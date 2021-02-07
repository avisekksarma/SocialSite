# just like urls.py of each apps for http routing,this is for websocket routing

from django.urls import path

from . import consumers

websocket_urlpatterns=[
    path('ws/chat/worldchat/',consumers.WorldChatConsumer.as_asgi(),name='chatconsumer')
]
