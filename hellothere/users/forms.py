from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import smtplib,ssl
import os
from .models import EmailCodeConfirmation
from email.message import EmailMessage
from django.contrib.auth.models import User
import random
from .multithreadworks import DeleteConfirmationCode


class LoginForm(forms.Form):
    error_css_class = 'error'   # REFERENCE=>  https://docs.djangoproject.com/en/3.1/ref/forms/api/#styling-required-or-erroneous-form-rows
    required_css_class = 'required'
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50,widget=forms.PasswordInput)
    
    

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50,help_text="Please type an legit email address.")
    password = forms.CharField(max_length=50,widget=forms.PasswordInput)
    
    def clean_username(self):
        cleaned_username = self.cleaned_data['username']
        if User.objects.filter(username=self.cleaned_data['username']):
            raise ValidationError(_('Such username already exists.'))
        return cleaned_username


    def clean_password(self):
        cleaned_password = self.cleaned_data['password']

        if len(cleaned_password) < 3:
            raise ValidationError(_('Password should be at least 3 characters long.'))
        for i in cleaned_password:
            if i in '0123456789':
                return cleaned_password
        raise ValidationError(_('Password should contain at least a number.'))

    def clean_email(self):

        if User.objects.filter(email=self.cleaned_data['email']):
            raise ValidationError(_('Such email already exists.')) 

        cleaned_email = self.cleaned_data['email']
        
        # variables for sending the email 

        port = 465   # is SSL so port number is 465
        smtp_server = 'smtp.gmail.com'
        sender_email = 'andrewsans2020@gmail.com'
        receiver_email = cleaned_email

        password = os.environ.get('PASS')

        msg = EmailMessage()
        msg['from'] = sender_email
        msg['to'] = receiver_email
        msg['subject'] = 'Code For Confirmation'

        confirmation_code = confirmationCode()
        email_confirmation = EmailCodeConfirmation(email=receiver_email,code = confirmation_code)
        
        DeleteConfirmationCode().make_thread(email_confirmation)

        email_confirmation.save()
        msg.set_content(f'''The code for your confirmation is:
        {confirmation_code}. 
        PLEASE DON\'T SHARE THIS WITH ANYONE. THE CODE EXPIRES IN 5 MINUTES.''')

        # creating a secure SSL context
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
                server.login(sender_email,password)
                server.send_message(msg)
        except Exception as e:
            print(e)
        
        return cleaned_email

class RegisterConfirmationForm(forms.Form):
    confirmation_code = forms.IntegerField()


def confirmationCode():
    random_code = []
    for _ in range(6):
        r = random.randint(0, 9)
        if _ == 0 and r == 0:
            while r == 0:
                r = random.randint(0,9)
        random_code.append(str(r))
    
    random_code = ''.join(random_code)
    random_code = int(random_code)
    return random_code

        
