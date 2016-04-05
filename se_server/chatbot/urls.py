__author__ = 'KAI'
from django.conf.urls import url,include
from django.contrib import admin
from chatbot import views
urlpatterns = [
    #The pages associated with chatbot
    url(r'personal',views.personalinfo,name='Personal Information'),
]
