from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request,'chat/index.html',{})


@login_required
def worldchat(request):
    context={
        'username':request.session.get('username')
    }
    return render(request,'chat/world_chat.html',context)
