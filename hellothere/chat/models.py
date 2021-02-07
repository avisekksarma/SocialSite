from django.db import models
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
filehandler = logging.FileHandler('chat/models.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(lineno)d:%(name)s:%(message)s')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)


class OnlineUsersInWorldChat(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'({self.user.username})'

    @classmethod
    def make_user_online(cls,username):
        user = User.objects.get(username=username)
        already_online_user = OnlineUsersInWorldChat.objects.filter(user=user)
        if not already_online_user:
            OnlineUsersInWorldChat(user=user).save()
        else:
            # this may happen if user without disconnecting tries to connect 
            # to the worldchat maybe via new device/browser/incognito/new tab
            pass
            

    @classmethod
    def make_user_offline(cls,username):
        user = User.objects.get(username=username)
        online_user = OnlineUsersInWorldChat.objects.get(user=user)
        online_user.delete()

    @staticmethod
    def serialize(**kwargs):
        if 'online_user_list' in kwargs:
            serialized_online_user_list=[]
            for online_user in kwargs['online_user_list']:
                serialized_online_user_list.append(
                    {
                        'username':online_user.user.username
                    }
                )
            logger.info(f'value: {serialized_online_user_list}')
            return serialized_online_user_list
