from django.shortcuts import render



def signup(request):
    return render(request, 'accounts/Signupform.html')


def loginview(request):
    return render(request, 'accounts/Signinform.html')


def logoutview(request):
    return render(request,'accounts/Signupform.html')
