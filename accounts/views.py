from django.db import transaction
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
                return render(request, 'jobs.html')
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
        skills = UserRecord[0].skills.replace('"', '').replace('[', '').replace(']', '').split(",")
        interests1 = UserRecord[0].interests.replace("'", "").replace(" ", "").replace("[", "").replace("]", "").split(
            ",")

        if UserRecord[0].gender == 'male':
            flag = True
        else:
            flag1 = True
        return render(request, 'EditProfile.html', {'UserRecord': UserRecord,
                                                    'UserEducation': UserEducations,
                                                    'UserExperience': UserExperiences,
                                                    "flag": flag,
                                                    "flag1": flag1,
                                                    "Skills": skills,
                                                    "Interests": interests1
                                                    })


@transaction.atomic
def updateinformation(request):
    flag = False
    flag1 = False
    if request.method == "POST":
        if request.user.is_authenticated():
            username = request.user.username
            if username == request.POST['email']:
                # Deleting the models from the signupModel,Django provided model
                # Deleting the Signup model automatically deletes the WorkExperiences,Educations Model
                User.objects.filter(username=username).delete()
                signupModel.objects.filter(email=username).delete()

                # Creating Everything new from here on
                user1 = User.objects.create_user(request.POST['email'], password=request.POST['password'])
                # Creating the user Signup Model
                signUpModel = signupModel.objects.create(user=user1, name=request.POST['name'],
                                                         dateofbirth=request.POST['dob'],
                                                         gender=request.POST.get('gender', None),
                                                         email=request.POST['email'],
                                                         password=request.POST['password'],
                                                         skills=json.dumps(request.POST.getlist('skills[]')),
                                                         interests=request.POST.getlist('interests[]'),
                                                         objectivestatement=request.POST['objstat'],
                                                         country=request.POST['country'], city=request.POST['City'])

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

                return render(request, 'jobs.html',
                              {'error': "Bio Updated Successfully"})
            else:
                flag = username_present(request.POST['email'])
                if flag == True:
                    username = request.user.username
                    UserRecord = models.signupModel.objects.filter(email=username)
                    UserEducations = models.Education.objects.filter(UserEducation=UserRecord)
                    UserExperiences = models.workexperienceModel.objects.filter(UserExperience=UserRecord)
                    skills = UserRecord[0].skills.replace('"', '').replace('[', '').replace(']', '').split(",")
                    interests1 = UserRecord[0].interests.replace("'", "").replace(" ", "").replace("[", "").replace("]",
                                                                                                                    "").split(
                        ",")

                    if UserRecord[0].gender == 'male':
                        flag = True
                    else:
                        flag1 = True

                    return render(request, 'EditProfile.html', {'UserRecord': UserRecord,
                                                                'UserEducation': UserEducations,
                                                                'UserExperience': UserExperiences,
                                                                "flag": flag,
                                                                "flag1": flag1,
                                                                "Skills": skills,
                                                                "Interests": interests1,
                                                                "error": "Email already taken please try a different email!"
                                                                })
                else:

                    # Deleting the models from the signupModel,Django provided model
                    # Deleting the Signup model automatically deletes the WorkExperiences,Educations Model
                    User.objects.filter(username=username).delete()
                    signupModel.objects.filter(email=username).delete()

                    # Creating Everything new from here on
                    user1 = User.objects.create_user(request.POST['email'], password=request.POST['password'])
                    # Creating the user Signup Model
                    signUpModel = signupModel.objects.create(user=user1, name=request.POST['name'],
                                                             dateofbirth=request.POST['dob'],
                                                             gender=request.POST.get('gender', None),
                                                             email=request.POST['email'],
                                                             password=request.POST['password'],
                                                             skills=json.dumps(request.POST.getlist('skills[]')),
                                                             interests=request.POST.getlist('interests[]'),
                                                             objectivestatement=request.POST['objstat'],
                                                             country=request.POST['country'], city=request.POST['City'])

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
                        temp1 = Education.objects.create(id=None,degree=listofdegrees[i],
                                                         institution=listofinstitution[i],
                                                         startdateedu=listofstartdate1[i],
                                                         enddateedu=listofenddate1[i], UserEducation=signUpModel)
                        ArrayContainingEducationObject.append(temp1)

                    for k in range(1, len(ArrayContainingEducationObject)):
                        ArrayContainingEducationObject[k].save()

                    return render(request, 'jobs.html',
                                  {'error': "Bio Updated Successfully"})

    return render(request, 'EditProfile.html')


def username_present(username):
    try:
        User.objects.get(username=username)
        return True
    except User.DoesNotExist:
        return False

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
