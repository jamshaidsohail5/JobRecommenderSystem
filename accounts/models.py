from django.db import models
from django.contrib.auth.models import User
from django.forms import DateField
from JobRecommenderSystem import settings


class signupModel(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    dateofbirth = DateField(input_formats = settings.DATE_INPUT_FORMATS)
    gender = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    skills = models.TextField(null=True)
    interests = models.TextField(null = True)
    objectivestatement = models.CharField(max_length=100)




class workexperienceModel(models.Model):
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    startDate = models.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    endDate = models.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    UserExperience = models.ForeignKey(signupModel, on_delete=models.CASCADE)





class Education(models.Model):
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    startdateedu = models.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    enddateedu = models.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    UserEducation = models.ForeignKey(signupModel,on_delete=models.CASCADE)
















