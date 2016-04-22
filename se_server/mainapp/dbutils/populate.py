
import csv


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','se_server.settings')
import django
django.setup()
from mainapp.models import Skill,JobPosting
"""
def get_mappings(filename):
    mappings={}
    with open(filename) as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            if(row[0]in mappings):
                mappings[row[0]].append(row[1])
            else:
                mappings[row[0]]=[row[1]]
    return mappings


def populate_skills(filename):
    with open(filename) as csvfile:
        reader=csv.reader(csvfile)
        count=0
        for row in reader:
            if(count==0):
                count+=1
                continue
            count+=1
            if(len(row[2])==0):
                continue
            try:
                s=Skill(id=count,name=row[2])
                s.save()
                print("SAVED "+s.name)
            except:
                pass

    #remove duplicates
    skill_names=[]
    for skill in Skill.objects.all():
        if(skill.name in skill_names):
            skill.delete()
        else:
            skill_names.append(skill.name)


def get_skills_from_position(position):
    skill_names=mappings[position]
    skills=[]
    for skill_name in skill_names:
        skill=Skill.objects.all().filter(name=skill_name)
        if(len(skill)==0):
            continue
        skills.append(skill[0])
    return skills

def populate_jobpostings(filename):
    with open(filename) as csvfile:
        reader=csv.reader(csvfile)
        count=0
        for row in reader:
            if(not count):
                count+=1
                continue
            count+=1
            location=row[1]
            industry=row[2]
            position=row[4]
            skills=get_skills_from_position(position)
            j=JobPosting(id=count,location=location,industry=industry,position=position)
            j.save()
            j.skills.add(*skills)
            j.save()
            print("SAVED:",str(j))
"""


def check_validity(filename):
    with open(filename) as csvfile:
        reader=csv.reader(csvfile)
        count=0
        wrong=0
        total=0
        for row in reader:
            if(not count):
                count+=1
                continue
            skills=row[3].split(",")
            skills=list(map(lambda x:x.strip(),skills))
            total+=len(skills)
            for skill in skills:
                #Model.objects.get(fieldname__contains=value)
                s=Skill.objects.all().filter(name=skill)
                if(not s):
                    s=Skill.objects.all().filter(name__icontains=skill)
                    if(len(s)==0):
                        #print(skill,"is not present")
                        wrong+=1
                    else:
                        print(s[0],"+++",skill)
                else:
                    #print(s[0],"____",skill)
                    pass

        print(wrong,total)

def populate_skills(filename):
    with open(filename) as csvfile:
        reader=csv.reader(csvfile)
        next(reader)
        for row in reader:
            print(row[0]+"-"+row[1]+"-"+row[2])
            if(row[2].strip()!=""):
                try:
                    s=Skill(id=int(row[0]),name=row[2])
                    s.save()
                except:
                    pass

def populate_jobpostings(filename):
    with open(filename) as csvfile:
        reader=csv.reader(csvfile)
        next(reader)
        count=0
        for row in reader:
            count+=1
            skill_set=[]
            skills=row[3].split(",")
            skills=list(map(lambda x:x.strip(),skills))
            for skill in skills:
                s=Skill.objects.all().filter(name=skill)
                if(s):
                    #print(s[0])
                    skill_set.append(s[0])
                if(not s):
                    s=Skill.objects.all().filter(name__icontains=skill)
                    if(len(s)==0):
                        pass
                        print("Skipping "+skill)
                    else:
                        #print(s[0])
                        skill_set.append(s[0])
            organization=row[0]
            location=row[1]
            industry=row[2]
            position=row[4]
            duration=row[5]
            stipend=row[6]
            url=row[7]
            type=row[8]
            print(row)
            j=JobPosting(id=count,organization=organization,location=location,industry=industry,link=url,type=type,stipend=int(stipend),position=position)
            j.save()
            j.skills.add(*skill_set)
            j.save()
            print(str(j))

from django.contrib.auth.models import User
from employers.models import OpenPositions
from django.contrib.auth import authenticate, login

def populate_openpositions():
    jobs=JobPosting.objects.all()
    for job in jobs:
        org=job.organization.replace(" ","_")
        user=authenticate(username=org,password=org)
        if(user is not None):
            o=OpenPositions.objects.all().filter(owner=user)
            if(not o):
                o=OpenPositions(owner=user)
                o.save()
                o.postings.add(job)
                o.save()
            else:
                o=o[0]
                o.postings.add(job)
                o.save()
        else:
            user=User.objects.create_user(org,org+"@"+org+".com",org)
            o=OpenPositions(owner=user)
            o.save()
            o.postings.add(job)
            o.save()

from mainapp.models import *
def populate_questions(filename):
    with open(filename,encoding="UTF-8",errors="ignore") as csvfile:
        reader=csv.reader(csvfile)
        next(reader)
        for row in reader:
            skill=row[0]
            s=Skill.objects.all().filter(name=skill)
            if(not s):
                continue
            s=s[0]
            q=Question(skill=s,name=row[1],optionA=row[2],optionB=row[3],optionC=row[4],optionD=row[5],answer=row[6])
            q.save()


def add_skills(slist,skillList):
    toAdd=[]
    for skill in slist:
        if(Skill.objects.all().filter(name=skill)):
            pass
        else:
            if(skill in skillList):
                s=skillList[skill]
                skill=Skill(name=skill)
                skill.save()
                toAdd.append(skill)
            else:
                print("SKIPPING",skill)
    return toAdd

def populate_skills_and_jobpostings(skillfilename,jobfilename):
    skills={}
    with(open(skillfilename)) as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            skills[row[1].strip()]=1
    print(skills)
    with open(jobfilename) as csvfile:
        reader=csv.reader(csvfile)
        next(reader)
        for row in reader:
            skill_list=row[3].split(",")
            print(skill_list)
            skill_list=list(map(lambda x:x.strip(),skill_list))
            toAdd=add_skills(skill_list,skills)
            j=JobPosting(location=row[1],industry=row[2],position=row[4],organization=row[0],link=row[7],type=row[8],stipend=int(row[6]))
            j.save()
            j.skills.add(*toAdd)
            j.save()
            print("ADDED",j)







if(__name__=="__main__"):

    os.environ.setdefault('DJANGO_SETTINGS_MODULE','justthejob.settings')
    import django
    django.setup()
    #populate_jobpostings("jl.csv")
    #mappings=get_mappings("skills_big.csv")
    #populate_skills_and_jobpostings("./KAI/datasets used/skills_big.csv","./KAI/datasets used/job listings_less_skills.csv")
    #populate_jobpostings("./KAI/datasets used/job listings_less_skills.csv")
    populate_openpositions()
    #populate_questions("./KAI/datasets used/questionnaire.csv")
    #for s in Skill.objects.all():
     #   s.delete()
    #populate_skills("skills_kai.csv")






