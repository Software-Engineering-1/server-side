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
def personalinfo(request):
    if(not request.session['user']):
        from authentication.views import login_user
        return redirect(login_user)
    if(request.method=='POST'):
        data=request.POST
        print("D",data)
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
            context={}
            return HttpResponse(template.render(context,request),status=200)
    else:
        template = loader.get_template('chatbot/ChatBot1.html')
        context={}
        return HttpResponse(template.render(context,request),status=200)

"""
last_name
age
 gender
 dob
 address
 phone_number


 user_details=models.OneToOneField(User, on_delete=models.CASCADE)
    age=models.IntegerField(null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)
    dob=models.DateField(null=False)
    address=models.CharField(max_length=100,null=False,default='The person has not specified their address yet')
    phone_regex = RegexValidator(regex=r'^[0-9]{10}$', message="Phone number must be entered in the format: '9999999999'.")
    phone_number = models.CharField(max_length=10,validators=[phone_regex], blank=True)
    resume_url=models.CharField(max_length=100,null=True)
 """