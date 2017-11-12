from django.http import HttpResponse
from django.shortcuts import render

from Models.models import Poll


def Signup(request):
    return render(request, 'Views/../accounts/template/Signupform.html')


def Signin(request):
    return render(request, 'Views/../accounts/template/Signinform.html')


