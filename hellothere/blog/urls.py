from django.urls import path

from . import views

urlpatterns = [
    path('', views.TestIndex.as_view(), name='index'),
]