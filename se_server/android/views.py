from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login     #Needed to work with default user model.

# Create your views here.

class ClientException(Exception):
    def __init__(self,name):
        Exception.__init__(self,name)
        self.name=name
    def __str__(self):
        return self.name


def login(request):
    if(request.method=="POST"):
        try:
            return do_login(request)
        except( ClientException) as e:
            return HttpResponse(str(e),status=400)
    else:
        return HttpResponse("Get request was sent. Not allowed",status=405)

def do_login(request):
    req={'user_name','password'}
    recv=set(request.POST.keys())
    missing=req-recv
    if(len(missing)>0):
        raise ClientException("Missing parameters "+str(missing))
    else:
        username=request.POST['user_name']
        password=request.POST['password']
        user=authenticate(username=username,password=password)  #Check if the username-password is valid
        if(user is None):
            return HttpResponse("Invalid credentials",status=400)
        else:
            return HttpResponse("Successfully logged in",status=200)
