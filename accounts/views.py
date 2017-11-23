from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from pandas._libs import json

from accounts.models import signupModel, workexperienceModel, Education


def signup(request):
    if request.method == "POST":
        try:
            User.objects.get(username=request.POST['username'])
            return render(request, 'Signupform.html', {'error': 'Email has already been taken!Try Another Mail'})
        except User.DoesNotExist:

            # print(request.POST['name'])
            # print(request.POST['dob'])
            #
            # answer = request.POST.get('gender', None)
            # print(answer)
            #
            # print(request.POST['username'])
            # print(request.POST['password'])
            #
            # print(request.POST.getlist("skills[]"))
            # print(request.POST.getlist("interests[]"))
            #
            # print(request.POST['Country'])
            # print(request.POST['City'])
            #
            # print(request.POST.getlist('Company[]'))
            # print(request.POST.getlist('Position[]'))
            # print(request.POST.getlist('startdates[]'))
            # print(request.POST.getlist('enddates[]'))
            #
            # print(request.POST.getlist('degreenames[]'))
            # print(request.POST.getlist('institution[]'))
            # print(request.POST.getlist('startdates1[]'))
            # print(request.POST.getlist('enddates1[]'))
            #
            # print(request.POST['textarea'])

            user1 = User.objects.create_user(request.POST['username'], password=request.POST['password'])
            #login(request, user1)

            signUpModel = signupModel.objects.create(user=user1, name=request.POST['name'],
                                                     dateofbirth=request.POST['dob'],
                                                     gender=request.POST.get('gender', None),
                                                     email=request.POST['username'],
                                                     password=request.POST['password'],
                                                     skills=json.dumps(request.POST.getlist('skills[]')),
                                                     interests=request.POST.getlist('interests[]'),
                                                     objectivestatement=request.POST['textarea'],
                                                     country=request.POST['Country'], city=request.POST['City'])

            signupModel.save()

            listofcompanies = request.POST.getlist('Company[]')
            listofpositions = request.POST.getlist('Position[]')
            listofstartdates = request.POST.getlist('startdates[]')
            listofenddates = request.POST.getlist('enddates[]')

            listofdegrees = request.POST.getlist('degreenames[]')
            listofinstitution = request.POST.getlist('institution[]')
            listofstartdate1 = request.POST.getlist('startdates1[]')
            listofenddate1 = request.POST.getlist('enddates1[]')

            ArrayContainingExperiencesObject = [
                workexperienceModel(id = None,company=listofcompanies[i], position=listofpositions[i],
                                    startDate=listofstartdates[i], endDate=listofenddates[i], UserExperience=user1) for
                i in
                len(listofcompanies)]

            for j in len(ArrayContainingExperiencesObject):
                ArrayContainingExperiencesObject[j].save()

            ArrayContainingEducationObject = [
                Education(id = None,degree=listofdegrees[i], institution=listofinstitution[i], startdateedu=listofstartdate1[i],
                          enddateedu=listofenddate1[i], UserEducation=user1) for i in len(listofdegrees)]

            for k in len(ArrayContainingEducationObject):
                ArrayContainingEducationObject[k].save()

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
        return render(request, 'Signupform.html')


def loginview(request):
    return render(request, 'Signinform.html')


def logoutview(request):
    return render(request, 'home.html')


'''
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

'''
