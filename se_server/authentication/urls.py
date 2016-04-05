__author__ = 'KAI'
__author__ = 'KAI'
from django.conf.urls import url,include
from django.contrib import admin
from authentication import views
urlpatterns = [
    #The pages associated with chatbot
    url(r'^$',views.homepage,name='Homepage'),
    url(r'^authentication/login',views.login_user,name="login"),
    url(r'^$',views.register,name='Register'),
    url(r'^auth/fp',views.fp,name="fp"),
]
