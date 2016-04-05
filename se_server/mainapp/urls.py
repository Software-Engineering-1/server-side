__author__ = 'KAI'
from django.conf.urls import url,include
from django.contrib import admin
from mainapp import views
urlpatterns = [
    #The pages associated with chatbot
    url(r'^test',views.mainView,name="test"),
]
