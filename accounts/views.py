from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from pandas._libs import json
from accounts import models
from accounts.models import signupModel, workexperienceModel, Education
import json as json1


# from accounts.models import signupModel
def signup(request):
    if request.method == "POST":
        try:
            User.objects.get(username=request.POST['username'])
            return render(request, 'Signupform.html', {'error': 'Email has already been taken!Try Another Mail'})
        except User.DoesNotExist:

            user1 = User.objects.create_user(request.POST['username'], password=request.POST['password'])

            # Creating the user Signup Model
            signUpModel = signupModel.objects.create(user=user1, name=request.POST['name'],
                                                     dateofbirth=request.POST['dob'],
                                                     gender=request.POST.get('gender', None),
                                                     email=request.POST['username'],
                                                     password=request.POST['password'],
                                                     skills=json.dumps(request.POST.getlist('skills[]')),
                                                     interests=request.POST.getlist('interests[]'),
                                                     objectivestatement=request.POST['textarea'],
                                                     country=request.POST['Country'], city=request.POST['City'])

            signUpModel.save()

            # Getting the list from the input tags
            listofcompanies = request.POST.getlist('Company[]')
            listofpositions = request.POST.getlist('Position[]')
            listofstartdates = request.POST.getlist('startdates[]')
            listofenddates = request.POST.getlist('enddates[]')

            listofdegrees = request.POST.getlist('degreenames[]')
            listofinstitution = request.POST.getlist('institution[]')
            listofstartdate1 = request.POST.getlist('startdates1[]')
            listofenddate1 = request.POST.getlist('enddates1[]')

            ArrayContainingExperiencesObject = []
            # Creating objects for the users
            for i in range(0, len(listofcompanies)):
                temp = workexperienceModel.objects.create(id=None,
                                                          company=listofcompanies[i],
                                                          position=listofpositions[i],
                                                          startDate=listofstartdates[i],
                                                          endDate=listofenddates[i],
                                                          UserExperience=signUpModel)
                ArrayContainingExperiencesObject.append(temp)

            for j in range(1, len(ArrayContainingExperiencesObject)):
                ArrayContainingExperiencesObject[j].save()

            ArrayContainingEducationObject = []
            for i in range(0, len(listofdegrees)):
                temp1 = Education.objects.create(id=None, degree=listofdegrees[i], institution=listofinstitution[i],
                                                 startdateedu=listofstartdate1[i],
                                                 enddateedu=listofenddate1[i], UserEducation=signUpModel)
                ArrayContainingEducationObject.append(temp1)

            for k in range(1, len(ArrayContainingEducationObject)):
                ArrayContainingEducationObject[k].save()

                # Setting the session
            login(request, user1)
            # UserRecord = models.signupModel.objects.filter(email=request.POST['username'])
            return render(request, 'jobs.html')
            # return render(request, 'MainPage.html', {'UserRecord': UserRecord})
    else:
        return render(request, 'Signupform.html')


def loginview(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username1'], password=request.POST['password1'])
        if user is not None:
            login(request, user)
            username = None
            if request.user.is_authenticated():
                # username = request.user.username
                # UserRecord = models.signupModel.objects.filter(email=username)
                # print("1")
                # print(UserRecord[0].name)
                # print("2")
                return render(request, 'jobs.html')
                # return render(request, 'MainPage.html', {'UserRecord': UserRecord})
        else:
            return render(request, 'Signinform.html', {'error': 'The user name and password didn\'t match.'})
    else:
        return render(request, 'Signinform.html')


def logoutview(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


def mainpageview(request):
    if request.user.is_authenticated():
        username = request.user.username
        UserRecord = models.signupModel.objects.filter(email=username)
        UserEducations = models.Education.objects.filter(UserEducation=UserRecord)
        UserExperiences = models.workexperienceModel.objects.filter(UserExperience=UserRecord)
        print("agya4")

        return render(request, 'MainPage.html', {'UserRecord': UserRecord,
                                                 'UserEducation': UserEducations,
                                                 'UserExperience': UserExperiences})


def editprofile(request):
    # Now here i ll retrieve all the credentials of the user from the
    # database and will display them on the page
    flag = False
    flag1 = False
    if request.user.is_authenticated():
        username = request.user.username
        UserRecord = models.signupModel.objects.filter(email=username)
        UserEducations = models.Education.objects.filter(UserEducation=UserRecord)
        UserExperiences = models.workexperienceModel.objects.filter(UserExperience=UserRecord)
        print(UserRecord[0].gender)
        if UserRecord[0].gender == 'male':
            flag = True
            print("1")
        else:
            print("2")
            flag1 = True
        return render(request, 'EditProfile.html', {'UserRecord': UserRecord,
                                                    'UserEducation': UserEducations,
                                                    'UserExperience': UserExperiences, "flag": flag, "flag1": flag1})

# return render_to_response("MainPage.html", {
#     'UserRecord': UserRecord, 'UserEducation': UserEducations,
#     'UserExperiences': UserExperiences,
# }, context_instance=RequestContext(request))

# print("agya5")

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
