from django.shortcuts import render

from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
# Create your views here.
from django.http import HttpResponse
#Just a placeholder to redirect to after login process is done
@csrf_exempt
def mainView(request):
    if(request.method=="POST"):
        from authentication.views import homepage
        request.session.pop("user",None)
        return redirect(homepage)
    else:
        template = loader.get_template('mainapp/test.html')    #Load the page
        context={'user':request.session.get("user",None)}               #Used for alerting on feedback submission
        return HttpResponse(template.render(context,request))       #render the page