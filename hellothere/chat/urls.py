from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='chat_index'),
    path('worldchat/',views.worldchat,name='worldchat'),
]
