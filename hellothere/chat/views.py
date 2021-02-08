from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .prev_worldchat import get_all_previous_worldchat_msgs

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

