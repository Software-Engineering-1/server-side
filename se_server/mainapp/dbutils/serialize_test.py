
import csv

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','se_server.settings')
import django
django.setup()
from mainapp.models import *
from mainapp.views import *
from django.core import serializers
from django.contrib.auth.models import *
if(__name__=="__main__"):

    os.environ.setdefault('DJANGO_SETTINGS_MODULE','se_server.settings')
    import django
    django.setup()
    context={}
    person1=User.objects.all().filter(username='kai123456')[0]
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
    with open('testdump.txt','w') as f:
        f.write(o)
    #
    #for s in Skill.objects.all():
     #   s.delete()
    #populate_skills("skills_kai.csv")





