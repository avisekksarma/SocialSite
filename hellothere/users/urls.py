from django.urls import path

from . import views

urlpatterns = [
    path('login/',views.login_user,name='login'),
    path('register/',views.register_user,name='register'),
    path('register/confirmation/<slug:random_url>',views.register_confirmation,name='register_confirmation'),
    path('logout/',views.logout_user,name="logout"),
    
#     path('account/register/',views.register,name='register'),
]
