import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import OnlineUsersInWorldChat,AllWorldChatMessages
from django.contrib.auth.models import User
from django.core import serializers

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
filehandler = logging.FileHandler('chat/consumers.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(lineno)d:%(name)s:%(message)s')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)



class WorldChatConsumer(WebsocketConsumer):

    def connect(self):
        logger.info('successfully connected')
        logger.warning(f'{self.scope}')
        # logger.warning(f'{request.session.get(email)}')
        # logger.warning(f'{request.session}')
        # accepts an incoming websocket connection
        # i.e. websocket handshaking is done.
        self.group_name = 'worldchat'

        
        OnlineUsersInWorldChat.make_user_online(self.scope['session']['username'])

        
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

        # self.send i.e. sending over the websocket can only happen after we accept the socket 
        # i.e. this function should be called after the self.accept function call
        
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'send_online_list',
            }
        )

    def disconnect(self,close_code):

        OnlineUsersInWorldChat.make_user_offline(self.scope['session']['username'])
        
        # this is done to update the online list when one user disconnects.

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'send_online_list',
            }
        )

    def receive(self,text_data):
        data_dict = json.loads(text_data)
        message = data_dict['message']
        sent_by = data_dict['sent_by']

        world_chat_msg = AllWorldChatMessages(sent_by=User.objects.get(username=sent_by),message=message)
        world_chat_msg.save()

        msg_sent_time = world_chat_msg.msg_sent_time 


        # self.send(text_data= json.dumps({'message':message}))

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'send_message',
                'message':message,
                'sent_by':sent_by,
                'msg_sent_time': world_chat_msg.serialize_datetime()
            }
        )

    def send_message(self,event):
        message=event['message']
        sent_by = event['sent_by']
        msg_sent_time = event['msg_sent_time']

        # event = {'type':'send_message','message':message }
        self.send(text_data=json.dumps({
            'message': message,
            'sent_by':sent_by,
            'msg_sent_time': msg_sent_time
        }))

    def send_online_list(self,event):
        self.send(text_data=json.dumps(return_all_online_users_dict(current_user=self)))

# returns all the online users except the current user/ user himself/herself.
def return_all_online_users_dict(current_user):

    return {
            'online_users': OnlineUsersInWorldChat.serialize(online_user_list=OnlineUsersInWorldChat.objects.exclude(user=User.objects.get(username=current_user.scope['session']['username'])))
        }
    