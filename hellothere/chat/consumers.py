import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import OnlineUsersInWorldChat,AllWorldChatMessages,AllPrivateChatMessages,IsFriendOnlineInPrivateChat
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

    online_list = OnlineUsersInWorldChat
    def connect(self):
        # logger.info('successfully connected')
        # logger.warning(f'{self.scope}')
        # logger.warning(f'{request.session.get(email)}')
        # logger.warning(f'{request.session}')
        # accepts an incoming websocket connection
        # i.e. websocket handshaking is done.
        self.group_name = 'worldchat'

        
        self.online_list.make_user_online(self.scope['session']['username'])

        # idk how we got self.channel_layer argument in the 
        # following line
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

        self.online_list.make_user_offline(self.scope['session']['username'])
        
        # this is done to update the online list when one user disconnects.

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'send_online_list',
            }
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self,text_data):
        data_dict = json.loads(text_data)
        message = data_dict['message']
        sent_by = data_dict['sent_by']

        world_chat_msg = AllWorldChatMessages(sent_by=User.objects.get(username=sent_by),message=message)
        world_chat_msg.save()



        # self.send(text_data= json.dumps({'message':message}))
        # sends the data to the backend of all the consumers 
        # who are in that group and then calls the function 
        # present in the following type key in each of those
        # consumers.
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                # due to following type key ,the 
                # send_message function of below is run in 
                # each consumer instance in group=worldchat
                #  (i.e. like each 
                # browser or tab opened which has open 
                # websocket connection after websocket 
                # handsake)
                'type':'send.message',
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
        # the following function sends data to the frontend (javascript).
        self.send(text_data=json.dumps({
            'message': message,
            'sent_by':sent_by,
            'msg_sent_time': msg_sent_time
        }))

    def send_online_list(self,event):
        self.send(text_data=json.dumps(return_all_online_users_dict(current_user=self,cls=self.online_list)))

# returns all the online users except the current user/ user himself/herself.
def return_all_online_users_dict(current_user,cls):

    return {
            'online_users': cls.serialize(online_user_list=cls.objects.exclude(user=User.objects.get(username=current_user.scope['session']['username'])))
        }
    


class PrivateChatConsumer(WebsocketConsumer):

    online_list = IsFriendOnlineInPrivateChat

    def connect(self):
        small_id = self.scope['url_route']['kwargs']['smallid']
        big_id = self.scope['url_route']['kwargs']['bigid']
        self.group_name = str(small_id)+'-'+str(big_id)

        self.online_list.make_user_online(self.scope['session']['username'])

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'send_online_list',
            }
        )

    def disconnect(self,close_code):
        self.online_list.make_user_offline(self.scope['session']['username'])

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type':'send_online_list',
            }
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
    
    def receive(self,text_data):
        data_dict = json.loads(text_data)
        message = data_dict['message']
        sent_by = data_dict['sent_by']

        private_chat_msg = AllPrivateChatMessages(sent_by=User.objects.get(username=sent_by),
        room_name=self.group_name,message=message)
        private_chat_msg.save()

        
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                
                'type':'send.message',
                'message':message,
                'sent_by':sent_by,
                'msg_sent_time': private_chat_msg.serialize_datetime()
            }
        )

    def send_message(self,event):
        message=event['message']
        sent_by = event['sent_by']
        msg_sent_time = event['msg_sent_time']

        # the following function sends data to the frontend (javascript).
        self.send(text_data=json.dumps({
            'message': message,
            'sent_by':sent_by,
            'msg_sent_time': msg_sent_time
        }))
    
    def send_online_list(self,event):
        self.send(text_data=json.dumps(return_all_online_users_dict(current_user=self,cls=self.online_list)))

