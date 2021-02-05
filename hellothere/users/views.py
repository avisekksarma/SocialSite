from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponsePermanentRedirect
from .forms import LoginForm,RegisterForm,RegisterConfirmationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import EmailCodeConfirmation
from django.http import HttpResponseNotFound
import string
import random


# Create your views here.

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                request.session['username'] = form.cleaned_data['username']
                # Redirect to a success page.
                messages.success(request,'You are succesfully logged in.')
                return redirect('index',permanent=True)
            # else:

    else:
        if request.session.get('_auth_user_backend') and request.session.get('_auth_user_hash') and request.session.get('_auth_user_id'):
            # this means logged in user
            return HttpResponseNotFound('<h1>Please logout to access this page.</h1>')
        form = LoginForm()
    context = {
        'form' : form,
    }
    return render(request,template_name="users/login.html",context=context)
        

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            
            # is_valid checks all the default validations like @ sign for email,others,
            # and also checks our custom validation 

            # storing the email in the session so that we check the email 
            # during the register confirmation time.
            request.session['username']=form.cleaned_data['username']
            request.session['email'] = form.cleaned_data['email']
            request.session['password'] = form.cleaned_data['password']
            new_random_url = ''.join(random.choices([ i for i in string.ascii_letters+string.digits ],k=16))
            request.session['random_url'] = new_random_url
            return HttpResponsePermanentRedirect(reverse('register_confirmation',kwargs={'random_url':new_random_url}))
    else:
        if request.session.get('_auth_user_backend') and request.session.get('_auth_user_hash') and request.session.get('_auth_user_id'):
            return HttpResponseNotFound('<h1>Please logout to access this page.</h1>')
        form = RegisterForm()
    context = {
        'form' : form,
    }
    return render(request,template_name="users/register.html",context=context)


def register_confirmation(request,random_url):
    if request.method == 'POST':
        form = RegisterConfirmationForm(request.POST)

        if form.is_valid():
            # following like makes sure if user entering the url is the one with same confirmation random url.
            if request.session.get('random_url')==random_url:
                try:
                    confirmation_code = form.cleaned_data['confirmation_code']
                    EmailCodeConfirmation.objects.get(email= request.session.get('email'),code = confirmation_code)

                    #  now only the user is eligible to be registered.
                    if request.session.get('username') and request.session.get('email') and request.session.get('password'):
                        User.objects.create_user(request.session.get('username'),request.session.get('email'),request.session.get('password'))
                        messages.success(request,'You are successfully registered.')
                        # del request.session.get('username')
                        try:
                            del request.session['email'] 
                            del request.session['password']
                            del request.session['random_url']
                        except:
                            pass
                        return redirect('index',permanent=True)
                except EmailCodeConfirmation.DoesNotExist:
                    # case when right user enters wrong confirmation code.
                    messages.error(request,'Wrong confirmation code.')

            else:
                # this is such a user who deleted cookies (sessionid) after the register process
                # or the user who just visited this url and tried to enter the code
                return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        # checking if the entered url by a user is equal to the random register url of the user entering it.
        if request.session.get('random_url')==random_url:
            form = RegisterConfirmationForm()
        else:
            # this user then must be an anonymous user 
            # or a logged in user who is not in registration process.
            return HttpResponseNotFound('<h1>Page not found</h1>')

    context ={
        'form':form
    }

    return render(request,template_name="users/register_confirmation.html",context = context)

def logout_user(request):
    logout(request)
    messages.success(request,'You are successfully logged out.')
    return redirect('login',permanent=True)