
import csv


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','se_server.settings')
import django
django.setup()
from mainapp.models import Skill,JobPosting

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

if(__name__=="__main__"):

    os.environ.setdefault('DJANGO_SETTINGS_MODULE','justthejob.settings')
    import django
    django.setup()
    mappings=get_mappings("skills_big.csv")
    #populate_skills("skills_kai.csv")
    populate_jobpostings("job_posting.csv")


