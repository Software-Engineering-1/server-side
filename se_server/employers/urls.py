__author__ = 'KAI'
from django.conf.urls import url,include
from django.contrib import admin
from employers import views
urlpatterns = [
    #The pages associated with chatbot
    url(r'login',views.login,name='Login'),
    url(r'home',views.home,name='Home'),
    url(r'showresume',views.showresume,name='Home'),
]
