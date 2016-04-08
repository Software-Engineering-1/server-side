from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.template import loader
from django.shortcuts import redirect
from mainapp.models import Personal
from mainapp.views import mainView
from django.contrib.auth.models import User
#from authentication.views import login_user
#View to handle personal information

def check_permissions(main_function):
    def _performchecks(request):
         if(not request.session['user']):
            from authentication.views import login_user
            return redirect(login_user)
         else:
             return main_function(request)
    return _performchecks


@check_permissions
def personalinfo(request):
    if(request.method=='POST'):
        data=request.POST
        age=int(data['age'])
        first_name=data['first_name']
        last_name=data['last_name']
        gender=data['gender']
        dob=data['dob']
        address=data['address']
        phone_number=data['phone_number']
        try:
            user=User.objects.all().filter(username=request.session['user'])[0]
            user.first_name=first_name
            user.last_name=last_name
            user.save()
            p=Personal(user_details=user,age=age,gender=gender,dob=dob,address=address,phone_number=phone_number,resume_url='')
            p.save()
            return redirect(mainView)
        except:
            template = loader.get_template('chatbot/ChatBot1.html')
            context={'error':1}
            return HttpResponse(template.render(context,request),status=200)
    else:
        template = loader.get_template('chatbot/ChatBot1.html')
        context={'error':0}
        return HttpResponse(template.render(context,request),status=200)

