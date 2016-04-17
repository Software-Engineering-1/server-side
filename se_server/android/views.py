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

@csrf_exempt
def add_skill(request):
    if(request.method=="POST"):
        try:
            return do_add_skill(request)
        except( ClientException) as e:
            return HttpResponse(str(e),status=400)
    else:
        return HttpResponse("Get request was sent. Not allowed",status=405)

@csrf_exempt
def add_publication(request):
    if(request.method=="POST"):
        try:
            return do_add_publication(request)
        except( ClientException) as e:
            return HttpResponse(str(e),status=400)
    else:
        return HttpResponse("Get request was sent. Not allowed",status=405)

@csrf_exempt
def add_person_organization(request):
    if(request.method=="POST"):
        try:
            return do_add_person_organization(request)
        except( ClientException) as e:
            return HttpResponse(str(e),status=400)
    else:
        return HttpResponse("Get request was sent. Not allowed",status=405)

@csrf_exempt
def remove_skill(request):
    if(request.method=="POST"):
        try:
            return do_remove_skill(request)
        except( ClientException) as e:
            return HttpResponse(str(e),status=400)
    else:
        return HttpResponse("Get request was sent. Not allowed",status=405)

def check_personal_deco(main_function):
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
                person = Personal.objects.all().filter(user_details = user)
                if(not person):
                    raise ClientException("Table in person entry does not exist with user "+user.username)
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
        user=User.objects.all().filter(username=data['user_name'])[0]
        if(Personal.objects.filter(user_details=user)):
           raise ClientException("Already filled in the details")
        try:
            age=int(data['age'])
            first_name=data['first_name']
            last_name=data['last_name']
            gender=data['gender']
            dob=data['dob']
            address=data['address']
            phone_number=data['phone_number']
            user=User.objects.all().filter(username=data['user_name'])[0]
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

@check_personal_deco
def do_add_skill(request):
    data = request.POST
    req = {'skill'}
    rcv = set(data.keys())
    missing = req - rcv
    if(len(missing) > 0):
        raise ClientException("Missing parameters "+str(missing))
    else:
        skill = data["skill"]
        s = Skill.objects.all().filter(name=skill)
        if(not s):
            raise ClientException("Skill "+skill +"is not present in the database")
        else:
            s=s[0]
        person1 = User.objects.all().filter(username = data['user_name'])[0]
        person = Personal.objects.all().filter(user_details = person1)[0]
        if(s in person.skills.all()):
            pass
        else:
            person.skills.add(s)
        try:
            person.save()
            return HttpResponse("Successfully added the skill", status = 200)
        except(Exception) as e:
            raise ClientException(str(e))

@check_personal_deco
def do_remove_skill(request):
    data = request.POST
    req = {'skill'}
    rcv = set(data.keys())
    missing = req - rcv
    if(len(missing) > 0):
        raise ClientException("Missing parameters "+str(missing))
    else:
        skill = data["skill"]
        s = Skill.objects.all().filter(name=skill)
        if(not s):
            raise ClientException("Skill "+skill +"is not present in the database")
        else:
            s=s[0]
        person1 = User.objects.all().filter(username = data['user_name'])[0]
        person = Personal.objects.all().filter(user_details = person1)[0]
        person_skills=person.skills.all()
        if(s in person_skills):
            person.skills.remove(s)
            person.save()
            return HttpResponse("Successfully removed skill "+skill,status=200)
        else:
            raise ClientException("Person does not have skill "+skill)

@check_personal_deco
def do_add_publication(request):
    data=request.POST
    req={'conference_name','topic','field_of_study','date_published'}
    recv=set(data.keys())
    missing=req-recv
    if(len(missing)>0):
        raise ClientException("Missing parameters "+str(missing))
    else:
        c_n=data["conference_name"]
        topic=data["topic"]
        fos=data["field_of_study"]
        date=data["date_published"]
        person1=User.objects.all().filter(username=data['user_name'])[0]
        person=Personal.objects.all().filter(user_details=person1)[0]
        try:
            p=Publications(conference_name=c_n,topic=topic,field_of_study=fos,date_published=date,author=person)
            p.save()
            return HttpResponse("Successfully added",status=200)
        except(Exception) as e:
            raise ClientException(str(e))

@check_personal_deco
def do_add_person_organization(request):
    data=request.POST
    req={'startDate','endDate','organization','title'}
    recv=set(data.keys())
    missing=req-recv
    if(len(missing)>0):
        raise ClientException("Missing parameters "+str(missing))
    else:
        startDate=data['startDate']
        endDate=data['endDate']
        person1=User.objects.all().filter(username=data['user_name'])[0]
        person=Personal.objects.all().filter(user_details=person1)[0]
        organization=data['organization']
        title=data['title']
        try:
            p=PersonOrganization(title=title,startDate=startDate,endDate=endDate,organization=organization,person=person)
            p.save()
            return HttpResponse("Successfully added",status=200)
        except(Exception) as e:
                raise ClientException(str(e))

@csrf_exempt
def add_project(request):
    if(request.method=="POST"):
        try:
            return do_add_project(request)
        except( ClientException) as e:
            return HttpResponse(str(e),status=400)
    else:
        return HttpResponse("Get request was sent. Not allowed",status=405)

@check_personal_deco
def do_add_project(request):
    data=request.POST
    req={'name','duration','url','description'}
    recv=set(data.keys())
    missing=req-recv
    if(len(missing)>0):
        raise ClientException("Missing parameters "+str(missing))
    else:
        name=data['name']
        person1=User.objects.all().filter(username=data['user_name'])[0]
        person=Personal.objects.all().filter(user_details=person1)[0]
        duration=int(data['duration'])
        url=data['url']
        description=data['description']
        context={}
        try:
            p=Project(name=name,duration=duration,url=url,description=description,person=person)
            p.save()
            return HttpResponse("Successfully added",status=200)
        except(Exception) as e:
                raise ClientException(str(e))

@csrf_exempt
def add_education(request):
    if(request.method=="POST"):
        try:
            return do_add_education(request)
        except( ClientException) as e:
            return HttpResponse(str(e),status=400)
    else:
        return HttpResponse("Get request was sent. Not allowed",status=405)

@check_personal_deco
def do_add_education(request):
    data=request.POST
    req={'name','grad_year','degree','field_of_study','score'}
    recv=set(data.keys())
    missing=req-recv
    if(len(missing)>0):
        raise ClientException("Missing parameters "+str(missing))
    else:
        name=data["name"]
        grad_year=data["grad_year"]
        degree=data["degree"]
        field_of_study=data["field_of_study"]
        score=data["score"]
        person1=User.objects.all().filter(username=data['user_name'])[0]
        person=Personal.objects.all().filter(user_details=person1)[0]
        try:
            p=Education(name=name,grad_year=grad_year,degree=degree,field_of_study=field_of_study,score=score,person=person)
            p.save()
            return HttpResponse("Successfully added",status=200)
        except(Exception) as e:
            raise ClientException(str(e))

@csrf_exempt
def get_details(request):
     if(request.method=="POST"):
        try:
            return do_get_details(request)
        except( ClientException) as e:
            return HttpResponse(str(e),status=400)
     else:
        return HttpResponse("Get request was sent. Not allowed",status=405)

from django.core import serializers

import json
def fill_context(username):
    context={}
    person1=User.objects.all().filter(username=username)[0]
    person=Personal.objects.all().filter(user_details=person1)
    j=serializers.serialize('json', person, indent=2,
    use_natural_foreign_keys=True, use_natural_primary_keys=True)
    k=json.loads(j)
    k[0]['fields']['user_details']={'user_name':person1.username,'first_name':person1.first_name,'last_name':person1.last_name,'email_id':person1.email}
    context['Personal']=k
    print(j)
    p=PersonOrganization.objects.all().filter(person=person)
    j=serializers.serialize('json', p, indent=2,
    use_natural_primary_keys=True,fields=('startDate','endDate','organization','title',))
    print(j)
    context['PersonOrganization']=json.loads(j)
    p=Publications.objects.all().filter(author=person)
    j=serializers.serialize('json', p, indent=2,
    use_natural_primary_keys=True,fields=('conference_name','topic','field_of_study','date_published',))
    print(j)
    context['Publications']=json.loads(j)
    p=Project.objects.all().filter(person=person)
    j=serializers.serialize('json', p, indent=2,
    use_natural_primary_keys=True,fields=('name','duration','url','description'))
    print(j)
    context['Project']=json.loads(j)
    p=Education.objects.all().filter(person=person)
    j=serializers.serialize('json', p, indent=2,
    use_natural_primary_keys=True,fields=('name','grad_year','degree','field_of_study','score',))
    print(j)
    context['Education']=json.loads(j)
    p=JobPosting.objects.all()
    pa=list(map(lambda x: x.job,JobApplication.objects.all().filter(applicant=person)))

    p=set(p)-set(pa)
    p=list(p)[:5]
    j=serializers.serialize('json', p, indent=2,
    use_natural_primary_keys=True,use_natural_foreign_keys=True)
    print(j)
    context['JobPosting']=json.loads(j)
    p=JobApplication.objects.all().filter(applicant=person)
    j=serializers.serialize('json', p, indent=2,use_natural_foreign_keys=True,fields=('job','score','date','status'))
    print(j)
    context['JobApplication']=json.loads(j)

    p=set(Skill.objects.all())-set(person[0].skills.all())
    j=serializers.serialize('json', p, indent=2,use_natural_foreign_keys=True)
    print(j)
    context['Skills']=json.loads(j)
    #mappings=get_mappings("skills_big.csv")
    #populate_skills("skills_kai.csv")
    #populate_jobpostings("joble.csv")
    o=json.dumps(context,indent=2)
    return o


@check_personal_deco
def do_get_details(request):
    data=request.POST
    ctx=fill_context(data['user_name'])
    return HttpResponse(ctx,status=200)



