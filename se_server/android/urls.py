"""justthejob URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from android import views
urlpatterns = [
    url(r'login',views.login,name="LOGIN"),
    url(r'register',views.register,name="REGISTER"),
    url(r'chatbot_details',views.submit_chatbot_details,name="CHATBOT"),
    url(r'add_skill',views.add_skill,name="ADD A NEW SKILL"),
    url(r'remove_skill',views.remove_skill,name="REMOVE A SKILL"),
    url(r'add_publication',views.add_publication,name="ADD PUBLICATION"),
    url(r'add_person_organization',views.add_person_organization,name="ADD ORGANIZATION"),
    url(r'add_project',views.add_project,name="ADD PROJECT"),
    url(r'add_education',views.add_education,name="ADD EDUCATION"),

    #url(r'register','authentication.views.register',name="Register"),
]
