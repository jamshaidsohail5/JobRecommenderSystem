from django.db import models
from django.contrib.auth.models import User
from django.forms import DateField
from JobRecommenderSystem import settings


class signupModel(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    dateofbirth = DateField(input_formats = settings.DATE_INPUT_FORMATS)
    gender = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    skills = models.TextField(null=True)
    interests = models.TextField(null = True)
    objectivestatement = models.CharField(max_length=100)




class workexperienceModel(models.Model):
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    startDate = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    endDate = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    workexp = models.ForeignKey(signupModel,related_name="workexpofuser")



class Education(models.Model):
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    startdateedu = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    enddateedu = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    educa = models.ForeignKey(signupModel,related_name="eduofuser")













