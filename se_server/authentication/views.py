from django.shortcuts import render     #Required to render our HTML (As in replace the python part in HTML with actual
from django.http import HttpResponse,HttpResponseRedirect   #Required to send HTTPResponse. A View should return one of these
# Create your views here.
from django.template import loader      #Required for loading our html
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User             #Need the default user model.
from django.contrib.auth import authenticate, login     #Needed to work with default user model.
from django.shortcuts import redirect                   #Needed to redirect
from chatbot.views import personalinfo
from mainapp.views import mainView
from .models import UserContact






"""
    This view is used to render the homepage.
    maps to authentication/index.html if no user is logged in.
    Loads their profile if they are already logged in
"""
@csrf_exempt
def homepage(request):
    if( request.session.get('user',None)):  #Check session object for user
        return redirect(mainView)           #exists, so redirect to profile
    if(request.method=="POST"):             #This post is used to handle feedback on website
        data=request.POST                   #Get the submitted fields like name,email and their message
        name=data['name']
        email=data['email']
        message=data['message']
        u=UserContact(name=name,email=email,message=message)
        u.save() #Save a 'UserContact' object to the database. The admin can then see feedback and respond with an email
        template = loader.get_template('authentication/index1.html')    #load the page
        context={'message':1}           #Set message to 1. Alert informing that feedback was submitted if this is 1
        return HttpResponse(template.render(context,request))   #render the page

    template = loader.get_template('authentication/index1.html')    #Load the page
    context={'message':0}               #Used for alerting on feedback submission
    return HttpResponse(template.render(context,request))       #render the page




"""
    This is the view used to handle the authentication page. maps to authentication/login.html template
    Upon login form submission, logs the user in if the credentials are correct. Alerts an error otherwise
    Upon register form submission, registers a new user to the database.Alerts an error if username is taken

"""

@csrf_exempt
def login_user(request):
    if(request.method=="POST"): #Means it is a post request
        data=request.POST       #Obtain data which was sent in the body. This is a dictionary
        if(data['title'])=='LOGIN': #I've 2 forms on same page.I've given different values to same key title to distinguish
            username=data['username']
            password=data['password']
            user=authenticate(username=username,password=password)  #Check if the username-password is valid
            if(user is not None):  #Yes. It is valid. So log the user in
                login(request,user) #Login . From this point. Can use request.user to get the user
                request.session['user']=user.username   #This is for remembering user across sessions
                return redirect(personalinfo)   #Important. Use this for redirecting him to different page after login
            else:   #He has entered wrong username/password. Load the login page itself again.
                template = loader.get_template('authentication/login.html')
                context={'error':2} #Show a js alert indicating wrong username.password for 2
                return HttpResponse(template.render(context,request))   #Show him the login page again
        elif(data['title'])=='REGISTER':    #The title is for register. Which means submit on register was clicked
            username=data['username']
            password=data['password']
            email=data['email']
            try:        #Throws exception if something goes wrong in creating. Typically username taken
                u=User.objects.create_user(username,email,password)
            except Exception as e:
                print(e)
                template = loader.get_template('authentication/login.html')
                context={'error':1} #Show js alert indicating username taken for 1
                return HttpResponse(template.render(context,request))   #Render back the login page
            else:   #No exception. User was created sucessfully
                u.save()    #Important. Save to database
                user=authenticate(username=username,password=password)  #Authenticate the new user in
                login(request,user)#Login the new user. ^We know authenticate will work. But login needs auth to be called
                request.session['user']=user.username
                return redirect(personalinfo)   #redirect him to the next page you intend to show
    else:   #GET request. Means he has loaded this url from browser. Show him our page
        template = loader.get_template('authentication/login.html')    #Load the page
        context={'error':0}                                         #No error needs to be shown
        return HttpResponse(template.render(context,request))       #Render the HTML page given the template and context

@csrf_exempt
def register(request):
    if(request.POST):
        data=request.POST
        username=data['username']
        password=data['password']
        email=data['email']

        try:
            u=User.objects.create_user(username,email,password)
        except Exception as e:
            print(e)
            template = loader.get_template('authentication/homepage.html')
            context={'error':1}
            return HttpResponse(template.render(context,request))
        else:
            u.save()
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect(personalinfo)
    else:
        template = loader.get_template('authentication/register.html')
        context={'error':0}
        return HttpResponse(template.render(context,request),status=200)

@csrf_exempt
def fp(request):
    if(request.method=="POST"):
        f=request.FILES['myfile']
        for s in f.chunks():
            print(s)
        return HttpResponse("HI")
    else:
        template = loader.get_template('authentication/fp.html')
        context={}
        return HttpResponse(template.render(context,request),status=200)




