from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='chat_index'),
    path('worldchat/',views.worldchat,name='worldchat'),
    path('search/',views.SearchPage.as_view(),name="search_users"),
    # privatechat part
    path('privatechat/<int:smallid>/<int:bigid>/',views.PrivateChat.as_view(),name='privatechat'),
    # api part
    path('makeurlforprivatechat/',views.makeurlforprivatechat,name='makeurlforprivatechat'),
    path('sendprivatechatuser/',views.send_current_opened_private_chat,name='send_current_opened_private_chat'),
    
]
