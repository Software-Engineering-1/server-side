from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.template import loader
from django.shortcuts import redirect
#from authentication.views import login_user
#View to handle personal information
def personalinfo(request):
    print(request.user)
    if(request.user.is_anonymous()):
        from authentication.views import login_user
        return redirect(login_user)
        #return redirect(login_user)
        pass
    #return HttpResponse("Test page. Yet to be designed",status=200)
    template = loader.get_template('chatbot/ChatBot1.html')
    context={}
    return HttpResponse(template.render(context,request),status=200)