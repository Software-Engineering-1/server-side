from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from mainapp.models import JobPosting

class OpenPositions(models.Model):
    owner=models.OneToOneField(User)
    postings=models.ManyToManyField(JobPosting)
