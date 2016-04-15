from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.shortcuts import redirect                   #Needed to redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_library
from django.template import loader      #Required for loading our html
from django.http import HttpResponse
from employers.models import OpenPositions
@csrf_exempt
def login(request):
    if(request.method=="POST"):
        data=request.POST
        username=data["username"]
        password=data["password"]
        user=authenticate(username=username,password=password)  #Check if the username-password is valid
        if(user is not None):  #Yes. It is valid. So log the user in
            login_library(request,user) #Login . From this point. Can use request.user to get the user
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

from mainapp.models import *


def fill_context(user):
    context={}
    context['user']=user
    p=Personal.objects.all().filter(user_details=user)[0]
    context['Personal']=p
    context['PersonOrganization']=PersonOrganization.objects.all().filter(person=p)
    context['Publication']=Publications.objects.all().filter(author=p)
    context['Project']=Project.objects.all().filter(person=p)
    context['Education']=Education.objects.all().filter(person=p)
    context["Skills"]=set(Skill.objects.all())-set(p.skills.all())
    return context



@csrf_exempt
def home(request):
    owner=User.objects.all().filter(username=request.session.get('user'))[0]
    jobs=OpenPositions.objects.all().filter(owner=owner)[0]
    job_context={}
    for job in jobs.postings.all():
        apps=JobApplication.objects.all().filter(job=job)
        app_contexts=[]
        for app in apps:
            """
            single_app_context={}
            single_app_context["name"]=app.applicant.user_details.username
            single_app_context["score"]=app.score
            single_app_context["date"]=app.date
            single_app_context["status"]=app.status
            """
            single_app_context=[]
            single_app_context.append(app.date)
            single_app_context.append(app.status)
            single_app_context.append(app.score)
            single_app_context.append(app.applicant.user_details.username)
            app_contexts.append(single_app_context)
        pos=job.position
        pos=pos.replace(" ","_")
        job_context[pos]=app_contexts
	#job_context["display_name"]=job.position
    context={'company-name':jobs.owner,'jobpostings':job_context}
    template=loader.get_template('employers/homepage.html')
    return HttpResponse(template.render(context,request))   #render the page

@csrf_exempt
def showresume(request):
    if(request.method=="POST" and request.POST.get("username",None)):
        person1=User.objects.all().filter(username=request.POST["username"])[0]
        context=fill_context(person1)
        template=loader.get_template('employers/showcandidateprofile.html')
        return HttpResponse(template.render(context,request))   #render the page
    elif(request.session.get('user',None)):
        redirect(login)
    else:
        redirect(home)
