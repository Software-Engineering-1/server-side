from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.shortcuts import redirect                   #Needed to redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import loader      #Required for loading our html
from django.http import HttpResponse

@csrf_exempt
def login(request):
    if(request.method=="POST"):
        data=request.POST
        username=data["username"]
        password=data["password"]
        user=authenticate(username=username,password=password)  #Check if the username-password is valid
        if(user is not None):  #Yes. It is valid. So log the user in
            login(request,user) #Login . From this point. Can use request.user to get the user
            request.session['user']=user.username   #This is for remembering user across sessions
            return redirect(home)
        else:
            template = loader.get_template('employers/login.html')    #load the page
            context={'message':1}           #Set message to 1. Alert informing that feedback was submitted if this is 1
            return HttpResponse(template.render(context,request))   #render the page
    else:
        template = loader.get_template('employers/login.html')    #load the page
        context={'message':0}           #Set message to 1. Alert informing that feedback was submitted if this is 1
        return HttpResponse(template.render(context,request))   #render the page

@csrf_exempt
def home(request):
    return HttpResponse("hello"+request.session["user"],status=200)