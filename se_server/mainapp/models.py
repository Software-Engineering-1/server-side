
from django.db import models

from django.contrib.auth.models import User
from django.core.validators import RegexValidator


GENDER_CHOICES=[('M','Male'),('F','Female')]
TITLE_CHOICES=[('Architectural and Engineering Managers', 'Architectural and Engineering Managers'), ('Auditors', 'Auditors'), ('Business Intelligence Analysts', 'Business Intelligence Analysts'), ('Business Teachers, Postsecondary', 'Business Teachers, Postsecondary'), ('Computer and Information Research Scientists', 'Computer and Information Research Scientists'), ('Computer and Information Systems Managers', 'Computer and Information Systems Managers'), ('Computer Hardware Engineers', 'Computer Hardware Engineers'), ('Computer Network Architects', 'Computer Network Architects'), ('Computer Network Support Specialists', 'Computer Network Support Specialists'), ('Computer Numerically Controlled Machine Tool Programmers, Metal and Plastic', 'Computer Numerically Controlled Machine Tool Programmers, Metal and Plastic'), ('Computer Programmers', 'Computer Programmers'), ('Computer Science Teachers, Postsecondary', 'Computer Science Teachers, Postsecondary'), ('Computer Systems Analysts', 'Computer Systems Analysts'), ('Computer User Support Specialists', 'Computer User Support Specialists'), ('Database Administrators', 'Database Administrators'), ('Electrical Engineering Technicians', 'Electrical Engineering Technicians'), ('Electronics Engineering Technicians', 'Electronics Engineering Technicians'), ('Engineering Teachers, Postsecondary', 'Engineering Teachers, Postsecondary'), ('Financial Quantitative Analysts', 'Financial Quantitative Analysts'), ('Graphic Designers', 'Graphic Designers'), ('Information Security Analysts', 'Information Security Analysts'), ('Mechatronics Engineers', 'Mechatronics Engineers'), ('Natural Sciences Managers', 'Natural Sciences Managers'), ('Operations Research Analysts', 'Operations Research Analysts'), ('Security Management Specialists', 'Security Management Specialists'), ('Software Developers, Applications', 'Software Developers, Applications'), ('Software Developers, Systems Software', 'Software Developers, Systems Software'), ('Telecommunications Engineering Specialists', 'Telecommunications Engineering Specialists'), ('Video Game Designers', 'Video Game Designers')]
TYPE_CHOICES=[('I','Internship'),('F','Full Time')]
DEGREE_CHOICES=[('H','High school'),('P','P U'),('M','Masters'),('B','Bachelors')]
class Skill(models.Model):
    name=models.CharField(max_length=100,null=False,unique=True)
    id=models.AutoField(primary_key=True,unique=True)
    def __str__(self):
        return str(self.id)+":"+self.name

class Personal(models.Model):
    user_details=models.OneToOneField(User, on_delete=models.CASCADE)
    age=models.IntegerField(null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)
    dob=models.DateField(null=False)
    address=models.CharField(max_length=100,null=False,default='The person has not specified their address yet')
    phone_regex = RegexValidator(regex=r'^[0-9]{10}$', message="Phone number must be entered in the format: '9999999999'.")
    phone_number = models.CharField(max_length=10,validators=[phone_regex], blank=True)
    resume_url=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.user_details.username



class PersonOrganization(models.Model):
    startDate=models.DateField()
    endDate=models.DateField()
    skills=models.ManyToManyField(Skill)
    person=models.ForeignKey(Personal,on_delete=models.CASCADE)
    organization=models.CharField(max_length=100,null=False)
    title=models.CharField(max_length=100, choices=TITLE_CHOICES, default='')                                  #Cannot get deleted
    def __str__(self):
        return self.person.user_details.username+":"+self.organization+":"+self.title
    class Meta:
        unique_together = (('person', 'organization','title'),)

class Publications(models.Model):
    conference_name=models.CharField(max_length=100,null=False)
    topic=models.CharField(max_length=100,null=False)
    field_of_study=models.CharField(max_length=100,null=False)
    author=models.OneToOneField(Personal)
    date_published=models.DateField()
    def __str__(self):
        return self.author.user_details.username+":"+self.conference_name

class JobPosting(models.Model):
    id=models.AutoField(primary_key=True)
    location=models.CharField(max_length=100)
    industry=models.CharField(max_length=100,null=False)
    skills=models.ManyToManyField(Skill)
    position=models.CharField(max_length=100,null=False)
    organization=models.CharField(max_length=100,null=False,default='')
    link=models.URLField(max_length=200,null=True)
    type=models.CharField(max_length=1,choices=TYPE_CHOICES,default='F')
    stipend=models.IntegerField(null=True)
    def __str__(self):
        return str(self.id)+":"+self.position+":"+self.organization

class Project(models.Model):
    person=models.ForeignKey(Personal)
    name=models.CharField(max_length=100)
    duration=models.IntegerField()
    url=models.URLField(max_length=200,null=True)
    description=models.CharField(max_length=500)
    def __str__(self):
        return str(self.person.user_details.username+":"+self.name)

class Education(models.Model):
    name=models.CharField(max_length=100)
    person=models.ForeignKey(Personal)
    grad_year=models.IntegerField()
    degree=models.CharField(max_length=100,choices=DEGREE_CHOICES)
    field_of_study=models.CharField(max_length=100)
    score=models.DecimalField(max_digits=6,decimal_places=2)
