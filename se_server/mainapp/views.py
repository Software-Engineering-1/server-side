from django.shortcuts import render

from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
# Create your views here.
from django.http import HttpResponse
from mainapp.models import Skill,Personal,JobPosting,PersonOrganization,Project,Education,Publications,JobApplication
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




def fill_context(user):
    context={}
    context['user']=user
    p=Personal.objects.all().filter(user_details=user)[0]
    context['Personal']=p
    context['PersonOrganization']=PersonOrganization.objects.all().filter(person=p)
    context['Publication']=Publications.objects.all().filter(author=p)
    j=JobPosting.objects.all()
    ja=list(map(lambda x: x.job,JobApplication.objects.all().filter(applicant=p)))

    j=set(j)-set(ja)
    j=list(j)[:5]
    context['jobs']=j
    context['Project']=Project.objects.all().filter(person=p)
    context['Education']=Education.objects.all().filter(person=p)
    context["Skills"]=set(Skill.objects.all())-set(p.skills.all())
    context["Publications"]=Publications.objects.all().filter(author=p)
    print(context)
    return context

@csrf_exempt
@check_permissions
def mainView(request):
    if(request.method=="POST"):
        data=request.POST
        type=data['type']
        if(type=="PersonOrganization"):
            startDate=data['startDate']
            endDate=data['endDate']
            person1=User.objects.all().filter(username=request.session.get('user'))[0]
            person=Personal.objects.all().filter(user_details=person1)[0]
            organization=data['organization']
            title=data['title']
            context={}
            try:
                p=PersonOrganization(title=title,startDate=startDate,endDate=endDate,organization=organization,person=person)
                p.save()
                context['submitted']=True
            except(Exception) as e:
                context['submitted']=str(e)
            finally:
                context.update(fill_context(person1))
                template = loader.get_template('mainapp/test.html')
                return HttpResponse(template.render(context,request))
        elif(type=="Project"):
            name=data['name']
            person1=User.objects.all().filter(username=request.session.get('user'))[0]
            person=Personal.objects.all().filter(user_details=person1)[0]
            duration=int(data['duration'])
            url=data['url']
            description=data['description']
            context={}
            try:
                p=Project(name=name,duration=duration,url=url,description=description,person=person)
                p.save()
                context['submitted']=True
            except(Exception) as e:
                context['submitted']=str(e)
            finally:
                context.update(fill_context(person1))
                template = loader.get_template('mainapp/test.html')
                return HttpResponse(template.render(context,request))
        elif(type=="Education"):
            name=data["name"]
            grad_year=data["grad_year"]
            degree=data["degree"]
            field_of_study=data["field_of_study"]
            score=data["score"]
            person1=User.objects.all().filter(username=request.session.get('user'))[0]
            person=Personal.objects.all().filter(user_details=person1)[0]
            context={}
            try:
                p=Education(name=name,grad_year=grad_year,degree=degree,field_of_study=field_of_study,score=score,person=person)
                p.save()
                context['submitted']=True
            except(Exception) as e:
                context['submitted']=str(e)
            finally:
                context.update(fill_context(person1))
                template = loader.get_template('mainapp/test.html')
                return HttpResponse(template.render(context,request))
        elif(type=="Logout"):
            from authentication.views import homepage
            request.session.pop("user",None)
            return redirect(homepage)
        elif(type=="addskill"):
            skill=data["skills"]
            s=Skill.objects.all().filter(name=skill)[0]
            person1=User.objects.all().filter(username=request.session.get('user'))[0]
            person=Personal.objects.all().filter(user_details=person1)[0]
            person.skills.add(s)
            person.save()
            context=fill_context(person1)
            context['submitted'] = 2
            template = loader.get_template('mainapp/test.html')
            return HttpResponse(template.render(context,request))
        elif(type=="removeskill"):
            skill=data["skillName"]
            s=Skill.objects.all().filter(name=skill)[0]
            person1=User.objects.all().filter(username=request.session.get('user'))[0]
            person=Personal.objects.all().filter(user_details=person1)[0]
            person.skills.remove(s)
            person.save()
            context=fill_context(person1)
            context['submitted'] = 2
            template = loader.get_template('mainapp/test.html')
            return HttpResponse(template.render(context,request))
        elif(type=="Publications"):
            c_n=data["conference_name"]
            topic=data["topic"]
            fos=data["field_of_study"]
            date=data["date_published"]
            person1=User.objects.all().filter(username=request.session.get('user'))[0]
            person=Personal.objects.all().filter(user_details=person1)[0]
            context={}
            try:
                p=Publications(conference_name=c_n,topic=topic,field_of_study=fos,date_published=date,author=person)
                p.save()
                context['submitted']=True
            except(Exception) as e:
                context['submitted']=str(e)
            finally:
                context.update(fill_context(person1))
                template = loader.get_template('mainapp/test.html')
                return HttpResponse(template.render(context,request))
        elif(type=="quiz"):
            score=float(data["score"])
            job_id=data["job_id"]
            person1=User.objects.all().filter(username=request.session.get('user'))[0]
            person=Personal.objects.all().filter(user_details=person1)[0]
            import datetime
            j=JobApplication(job=JobPosting.objects.all().filter(id=job_id)[0],applicant=person,score=score)
            j.save()
            context={}
            context['submitted'] = 2
            context.update(fill_context(person1))
            template = loader.get_template('mainapp/test.html')
            return HttpResponse(template.render(context,request))


    else:
        template = loader.get_template('mainapp/test.html')    #Load the page
        context={'user':request.session.get("user",None)}               #Used for alerting on feedback submission
        p=Personal.objects.all().filter(user_details=User.objects.all().filter(username=request.session['user'])[0])[0]
        u=User.objects.all().filter(username=request.session['user'])[0]
        context=fill_context(u)
        context['submitted'] = 2
        return HttpResponse(template.render(context,request))       #render the page



class Question:
    def __init__(self,skill,question,choices,correct):
        self.skill=skill
        self.question=question
        self.choices=choices
        self.correct=correct

import csv
@csrf_exempt
def quiz(request):
    if(request.method=="POST"):
        data=request.POST
        job_id=data["type"]
        j=JobPosting.objects.all().filter(id=job_id)[0]
        """
        skills=j.skills.all()
        import random
        random.shuffle(skills)
        skills=skills[:3]
        skills=list(map(lambda x:x.name,skills))
        """
        questions=[]
        skills=["JavaScript","C#","PHP"]
        with open("mainapp/dbutils/questions.csv",encoding="UTF-8",errors="ignore") as csvfile:
            question={}
            reader=csv.reader(csvfile)
            next(reader)
            count=0
            for row in reader:
                if(count==4):
                    break
                if(row[0] in skills):
                    questions.append(Question(row[0],row[1],[row[2],row[3],row[4],row[5]],row[6]))
                    count+=1
        template = loader.get_template('quiz/quiz.html')    #Load the page
        context={'questions':questions,'job_id':job_id}               #Used for alerting on feedback submission
        return HttpResponse(template.render(context,request))


    else:
        return redirect(mainView)


@csrf_exempt
def dashboard(request):
    template = loader.get_template('mainapp/dashboard.html')    #Load the page
    person1=User.objects.all().filter(username=request.session.get('user'))[0]
    person=Personal.objects.all().filter(user_details=person1)[0]
    j=JobApplication.objects.all().filter(applicant=person)
    #print(j)
    context={'Applications':j}               #Used for alerting on feedback submission
    return HttpResponse(template.render(context,request))
