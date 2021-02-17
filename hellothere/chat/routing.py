# just like urls.py of each apps for http routing,this is for websocket routing

from django.urls import path

from . import consumers


websocket_urlpatterns=[
    path('ws/chat/worldchat/',consumers.WorldChatConsumer.as_asgi(),name='chatconsumer'),
    # TODO: (NOT a todo just highlighted thing ) Dont 
    # forget to put a trailing slash in the url 
    path('ws/chat/privatechat/<int:smallid>/<int:bigid>/',consumers.PrivateChatConsumer.as_asgi(),name='privatechatconsumer')
]
