from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login     #Needed to work with default user model.
from django.views.decorators.csrf import csrf_exempt
from mainapp.models import *
# Create your views here.

class ClientException(Exception):
    def __init__(self,name):
        Exception.__init__(self,name)
        self.name=name
    def __str__(self):
        return self.name

#/android/login
@csrf_exempt
def login(request):
    if(request.method=="POST"):
        try:
            return do_login(request)
        except( ClientException) as e:
            return HttpResponse(str(e),status=400)
    else:
        return HttpResponse("Get request was sent. Not allowed",status=405)

#/android/register
@csrf_exempt
def register(request):
    if(request.method=="POST"):
        try:
            return do_register(request)
        except(ClientException) as e:
            return HttpResponse(str(e),status=400)
    else:
        return HttpResponse("Get request was sent. Not allowed",status=405)

#/android/chatbot_details
@csrf_exempt
def submit_chatbot_details(request):
    if(request.method=="POST"):
        try:
            return do_submit_chatbot_details(request)
        except(ClientException) as e:
            return HttpResponse(str(e),status=400)
    else:
        return HttpResponse("Get request was sent. Not allowed",status=405)

def check_credentials_deco(main_function):
    def _performchecks(request):
        req={'user_name','password'}
        recv=request.POST.keys()
        missing=req-recv
        if(len(missing)>0):
            raise ClientException("Missing parameters "+str(missing))
        else:
            username=request.POST['user_name']
            password=request.POST['password']
            user=authenticate(username=username,password=password)  #Check if the username-password is valid
            if(user is None):
                raise ClientException("Invalid Credentials")
            else:
                return main_function(request)
    return _performchecks

@check_credentials_deco
def do_submit_chatbot_details(request):
    req={'age','gender','dob','address','phone_number','first_name','last_name'}
    recv=request.POST.keys()
    missing=req-recv
    if(len(missing)>0):
        raise ClientException("Missing parameters "+str(missing))
    else:
        data=request.POST
        try:
            age=int(data['age'])
            first_name=data['first_name']
            last_name=data['last_name']
            gender=data['gender']
            dob=data['dob']
            address=data['address']
            phone_number=data['phone_number']
            user=User.objects.all().filter(username=request.session['user'])[0]
            user.first_name=first_name
            user.last_name=last_name
            user.save()
            p=Personal(user_details=user,age=age,gender=gender,dob=dob,address=address,phone_number=phone_number,resume_url='')
            p.save()
            return HttpResponse("Successfully updated details",status=200)
        except(Exception) as e:
            raise ClientException(str(e))

def do_register(request):
    req={'user_name','password','email_id'}
    recv=set(request.POST.keys())
    missing=req-recv
    if(len(missing)>0):
        raise ClientException("Missing parameters "+str(missing))
    else:
        username=request.POST['user_name']
        password=request.POST['password']
        email_id=request.POST['email_id']
        try:
            u=User.objects.create_user(username=username,email=email_id,password=password)
            u.save()
            return HttpResponse("Successfully registered",status=200)
        except:
            raise ClientException("Username already taken")

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
            raise ClientException("Invalid Credentials")
        else:
            return HttpResponse("Successfully logged in",status=200)
