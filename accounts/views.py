from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from pandas._libs import json

from accounts.models import signupModel, workexperienceModel, Education


def signup(request):

    print("1")
    if request.method == "POST":
        try:
            print("2")
            User.objects.get(username=request.POST['username'])
            return render(request, 'Signupform.html', {'error': 'Email has already been taken!Try Another Mail'})
            print("3")
        except User.DoesNotExist:
            print("4")
            if (request.POST['name'] and request.POST['dob'] and request.POST.get('gender') and request.POST[
                'username'] and
                    request.POST['password'] and request.POST.getlist('skills[]') and request.POST.getlist(
                'interests[]') and request[
                'Country'] and
                    request.POST['City'] and request.POST.getlist('Company[]') and request.POST.getlist(
                'Position[]') and request.POST.getlist(
                'startdates[]') and
                    request.POST.getlist('enddates[]') and request.POST.getlist(
                'degreenames[]') and request.POST.getlist('institution[]') and
                    request.POST.getlist('startdates1[]') and
                    request.POST.getlist('enddates1[]') and request.POST['objstat']):
                print("5")
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
                print("6")
                login(request, user)
                print("7")
                signUpModel = signupModel.objects.create(name=request.POST['name'], dateofbirth=request.POST['dob'],
                                                         gender=request.POST.get['gender'],
                                                         email=request.POST['username'],
                                                         password=request.POST['password'],
                                                         skills=json.dumps(request.POST.getlist('skills[]')),
                                                         interests=request.POST.getlist('interests[]'),
                                                         objectivestatement=request.POST['objstat'],
                                                         country=request.POST['Country'], city=request.POST['City'])
                print("8")

                listofcompanies = request.POST.getlist('Company[]')
                listofpositions = request.POST.getlist('Position[]')
                listofstartdates = request.POST.getlist('startdates[]')
                listofenddates = request.POST.getlist('enddates[]')
                print("9")

                listofdegrees = request.POST.getlist('degreenames[]')
                listofinstitution  = request.POST.getlist('institution[]')
                listofstartdate1 = request.POST.getlist('startdates1')
                listofenddate1 = request.POST.getlist('enddates1')

                print("9")

                for i in len(listofcompanies):
                    signupModel.workexpofuser.create(company = listofcompanies[i] ,position = listofpositions[i],
                                                     startDate = listofstartdates[i] ,endDate = listofenddates[i] )
                print("10")

                for i in len(listofdegrees):
                    signupModel.eduofuser.create(degree = listofdegrees[i], institution=listofinstitution[i],
                                                     startdateedu=listofstartdate1[i], enddateedu=listofenddate1[i])
                print("11")

                # signupModel.name = request.POST['name']
                # signupModel.dateofbirth = request.POST['dob']
                # signupModel.gender = request.POST.get('gender')
                # signupModel.email = request.POST['username']
                # signupModel.password = request.POST['password']
                # signupModel.skills = json.dumps(request.POST.getlist('skills[]'))
                # signupModel.interests = json.dumps(request.POST.getlist('interests[]'))
                # signupModel.objectivestatement = request.POST['objstat']
                # signupModel.country = request.POST['Country']
                # signupModel.city = request.POST['City']




                return render(request, 'MainPage.html')
            else:
                return render(request, 'Signupform.html',
                              {'error': 'ERROR: Some Fields missing'})
    else:
        return render(request, 'Signupform.html')


def loginview(request):
    return render(request, 'Signinform.html')


def logoutview(request):
    return render(request, 'home.html')
