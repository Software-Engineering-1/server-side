from django.shortcuts import render

from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
# Create your views here.
from django.http import HttpResponse
from mainapp.models import Personal,JobPosting
from django.contrib.auth.models import User


#Just a placeholder to redirect to after login process is done



def check_permissions(main_function):
    def _performchecks(request):
        if(not request.session.get('user',None)):
            from authentication.views import login_user
            return redirect(login_user)
        else :
            p=Personal.objects.all().filter(user_details=User.objects.all().filter(username=request.session['user']))
            if(len(p)==0):
                from chatbot.views import personalinfo
                return redirect(personalinfo)
            else:
                return main_function(request)
    return _performchecks


@csrf_exempt
@check_permissions
def mainView(request):
    if(request.method=="POST"):
        from authentication.views import homepage
        request.session.pop("user",None)
        return redirect(homepage)
    else:
        template = loader.get_template('mainapp/test.html')    #Load the page
        context={'user':request.session.get("user",None)}               #Used for alerting on feedback submission
        p=Personal.objects.all().filter(user_details=User.objects.all().filter(username=request.session['user'])[0])[0]
        u=User.objects.all().filter(username=request.session['user'])[0]
        context['user']=u
        context['details']=p
        j=JobPosting.objects.all()[:5]
        context['jobs']=j
        return HttpResponse(template.render(context,request))       #render the page