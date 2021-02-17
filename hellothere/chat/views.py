from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse,HttpResponseNotAllowed,HttpResponseNotFound
from django.contrib.auth.models import User
from django.views.generic import ListView
from .prev_worldchat import get_all_previous_worldchat_msgs,get_all_previous_private_msgs
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View

import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
filehandler = logging.FileHandler('chat/views.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(lineno)d:%(name)s:%(message)s')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)


@login_required
def index(request):
    return render(request,'chat/index.html',{})


@login_required
def worldchat(request):
    context={
        'username':request.session.get('username'),
        'all_previous_msgs':get_all_previous_worldchat_msgs()
    }
    return render(request,'chat/world_chat.html',context)

@method_decorator(csrf_exempt, name='dispatch')
class SearchPage(ListView):
    model = User

    def get(self,*args,**kwargs):
        
        #  seems like args[0] is request object.
        # print(args[0].session['username'])
        request = args[0]
        return render(request,'chat/search.html',{})

    
    def post(self,*args,**kwargs):
        request = args[0]
        data = json.loads(request.body)

        if (data.get('search')):
            searched_users = User.objects.filter(username__icontains=data.get('search'))
            searched_users_username = {'users':[user.username for user in searched_users]}

            return JsonResponse(data=searched_users_username)
        else:
            return JsonResponse(data={'no_users':"Please search for a username (don't submit empty)."})
        
@login_required
@csrf_exempt
def makeurlforprivatechat(request):
    logger.error(request.method)
    logger.error(type(request.method))
    if (request.method != 'POST'):
        return HttpResponseNotAllowed(['POST'])
    else:
        data = json.loads(request.body)
        id1 = User.objects.get(username=data['requested_user']).id
        id2 = User.objects.get(username=data['my_username']).id
        if id1<id2:
            url = str(id1)+'/'+str(id2)
        else:
            url = str(id2)+'/'+str(id1)
        return JsonResponse(data={'url':url})

@login_required
@csrf_exempt
def send_current_opened_private_chat(request):
    logger.error(request.user.username)
    if (request.method != 'POST'):
        return HttpResponseNotAllowed(['POST'])
    else:
        data = json.loads(request.body)
        request.session['latest_private_user_for_chat'] = data['current_private_user']
        return JsonResponse(data={'message':'success'},status_code=200)


class  PrivateChat(LoginRequiredMixin,View):
    
    def get(self,request,smallid,bigid):
        try:
            user1 = User.objects.get(pk=smallid)
            user2 = User.objects.get(pk=bigid)
        except User.DoesNotExist:
            return HttpResponseNotFound('<h1>Page not found</h1>')

        # case when a malicious user hits first id 
        # argument to be bigger than the second id
        # argument ( say like chat/.../9/4/)
        if user1.id > user2.id:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        
        if user1.username == request.session.get('username'):
            my_username = user1.username
            friend_username = user2.username
        elif user2.username == request.session.get('username'):
            my_username= user2.username
            friend_username = user1.username
        else:
            # case when the get request is made by a user who doesnt have his id in the url
            # i.e. like seeing other users' private chat.
            return HttpResponseNotFound('<h1>Page not found</h1>')
        context={
        'my_username':my_username,
        'friend_username': friend_username,
        'small_id':smallid,
        'big_id':bigid,
        'all_previous_msgs':get_all_previous_private_msgs(str(smallid)+'-'+str(bigid))
    }
        return render(request,'chat/private_chat.html',context)

