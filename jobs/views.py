import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from pymongo import MongoClient
from accounts import models

jobs = []


class Jobs(object):
    # Note that we're taking an argument besides self, here.
    def __init__(self, id=0, jobTitle="", jobCompany="", jobLocation="", jobSalary="", jobSummary="", jobLink=""):
        self.id = id
        self.jobTitle = jobTitle
        self.jobCompany = jobCompany
        self.jobLocation = jobLocation
        self.jobSalary = jobSalary
        self.jobSummary = jobSummary
        self.jobLink = jobLink


def jobsviewing(request):
    return render(request, 'jobs.html')


# This Function Stores Implicit Feedback
def displayingJobDetail(request):
    if request.method == "POST":
        global jobs
        connection = MongoClient(port=27017)

        implicitFbDB = connection.ImplicitFeedback
        jobsDB = connection.Jobs

        # Here I will first get the Job id from the Hidden Text Box
        JobID = [key for key in request.POST if key.startswith("jobId")]

        # Getting the username
        username = request.user.username

        # Now retrieving the Django object corresponding to it from the Sqlite3 Database
        UserRecord = models.signupModel.objects.filter(email=username)

        # Getting the Job
        Number = JobID[0].split("+")
        print("Job id is ", Number[1])
        job_retrieved_to_be_displayed = jobs[int(Number[1]) - 1]

        jobId = 1
        jobDetailsCollection = jobsDB.jobsDetail
        #there is no job in Jobs Database
        if jobDetailsCollection.count() == 0:
            Job = {
                'userassignedId': jobId,
                'JobTitle': job_retrieved_to_be_displayed.jobTitle,
                'JobCompany': job_retrieved_to_be_displayed.jobCompany,
                'JobLocation': job_retrieved_to_be_displayed.jobLocation,
                'JobSalary': job_retrieved_to_be_displayed.jobSalary,
                'JobSummary': job_retrieved_to_be_displayed.jobSummary,
            }
            result = jobDetailsCollection.insert_one(Job)

        #Jobs Database is not empty
        else:
            # check if the job already exists or not
            jobsData = jobDetailsCollection.find_one({"JobTitle": job_retrieved_to_be_displayed.jobTitle})

            #If does not exists, retrieve the number of jobs and assign count+1 as jobId
            if jobsData is None:
                no_of_documents = jobDetailsCollection.count();
                jobId = no_of_documents + 1
                Job = {
                    'userassignedId': jobId,
                    'JobTitle': job_retrieved_to_be_displayed.jobTitle,
                    'JobCompany': job_retrieved_to_be_displayed.jobCompany,
                    'JobLocation': job_retrieved_to_be_displayed.jobLocation,
                    'JobSalary': job_retrieved_to_be_displayed.jobSalary,
                    'JobSummary': job_retrieved_to_be_displayed.jobSummary,
                }
                result = jobDetailsCollection.insert_one(Job)
            else:
                jobId = jobsData['userassignedId']

        #If the user has rated the job before
        feed_back_of_user = implicitFbDB.reviews.find_one({"Userid": UserRecord[0].idformongo, "Jobid": jobId})


        #If he hadn't
        if feed_back_of_user is None:
            print("Nothing initially in the DB")
            implicit_feedback_count = 1
            Feedback = {
                'Userid': UserRecord[0].idformongo,
                'Jobid': jobId,
                'ImplicitRating': implicit_feedback_count
            }
            result = implicitFbDB.reviews.insert_one(Feedback)
        #f he had
        else:
            # This means that the User has already opened this job and gave implplicit rating
            # So increasing the previous count Would do the job
            # Incrementing the Job Implicit Rating
            implicitFbDB.reviews.update(
                {'Userid': UserRecord[0].idformongo, 'Jobid': jobId},
                {
                    "$inc": {"ImplicitRating": 1}
                }
            )

        return render(request, 'jobsDetail.html', {"jobsDetail": job_retrieved_to_be_displayed})


def jobsretrieving(request):
    print("ab to ayaa")
    if request.method == "POST":
        print("aya zaroor")

        global jobs
        jobs = []

        id_temp = ""
        jobTitle_temp = ""
        jobCompany_temp = ""
        jobLocation_temp = ""
        jobSalary_temp = ""
        jobSummary_temp = ""
        jobLink_temp = ""

        desc = "web"
        loc = ""
        j = 1
        start = 0

        while start is not 20:
            r = requests.get("https://www.indeed.com/jobs?q=" + request.POST['keyword'] + "&l=" + request.POST[
                'location'] + "&start=" + str(start),
                             proxies={"http": "http://61.233.25.166:80"})
            start += 10
            data = r.text
            soup = BeautifulSoup(data, 'lxml')
            soup = soup.findAll("a", {"class": "turnstileLink"})

            for link in soup:
                jobLink = link.get("href")
                if "clk" in jobLink:
                    jobRequest = requests.get("https://www.indeed.com" + jobLink,
                                              proxies={"http": "http://61.233.25.166:80"})
                    jobData = jobRequest.text
                    jobSoup = BeautifulSoup(jobData, 'lxml')

                    id_temp = j

                    print("JobID", id_temp)

                    jobTitle = jobSoup.find("b", {"class": "jobtitle"})
                    jobData = jobTitle.text

                    jobTitle_temp = jobTitle.text

                    print("JobTitle", jobTitle_temp)

                    jobCompany = jobSoup.find("span", {"class": "company"})

                    if jobCompany:
                        jobData = jobData + " " + jobCompany.text
                        jobCompany_temp = jobCompany.text

                        print(jobCompany_temp)

                    jobLocation = jobSoup.find("span", {"class": "location"})

                    if jobLocation:
                        jobData = jobData + " " + jobLocation.text
                        jobLocation_temp = jobLocation.text

                        print(jobLocation_temp)

                    jobSalary = jobSoup.find("span", {"class": "no-wrap"})
                    if jobSalary:
                        jobData = jobData + " " + jobSalary.text
                        jobSalary_temp = jobSalary.text

                        print(jobSummary_temp)

                    jobApplyLink = jobSoup.find("a", {"class": "view_job_link view-apply-button blue-button"})
                    if jobApplyLink:
                        jobApplyLink = "https://www.indeed.com" + jobApplyLink.get("href")
                        jobLink_temp = jobApplyLink
                        print(jobApplyLink)

                    jobSummary = jobSoup.find("span", {"class": "summary"})
                    if jobSummary:
                        jobData = jobData + " " + jobSummary.text
                        jobSummary_temp = jobSummary.text

                        # print(jobSummary_temp)

                    jobs.append(Jobs(id_temp, jobTitle_temp, jobCompany_temp, jobLocation_temp, jobSalary_temp,
                                     jobSummary_temp, jobLink_temp))
                    j += 1
        return render(request, 'jobs.html', {"jobList": jobs})

    else:
        return render(request, 'jobs.html')

def saveExplicitRating(request):
    if request.method == "POST":
        global jobs
        connection = MongoClient(port=27017)
        explicitFbDB = connection.ExplicitFeedback
        jobsDB = connection.Jobs

        actual_star_number_and_job_number = request.POST.get('star')

        # Getting the username
        username = request.user.username

        # Now retrieving the Django object corresponding to it from the Sqlite3 Database
        UserRecord = models.signupModel.objects.filter(email=username)

        # Getting the JobTitle
        Number = actual_star_number_and_job_number.split("+")
        print("Star Rating is", Number[1])
        print("Job id is ", Number[2])

        job_retrieved_to_be_displayed = jobs[int(Number[2]) - 1]

        jobId = 1
        jobDetailsCollection = jobsDB.jobsDetail
        # there is no job in Jobs Database
        if jobDetailsCollection.count() == 0:
            Job = {
                'userassignedId': jobId,
                'JobTitle': job_retrieved_to_be_displayed.jobTitle,
                'JobCompany': job_retrieved_to_be_displayed.jobCompany,
                'JobLocation': job_retrieved_to_be_displayed.jobLocation,
                'JobSalary': job_retrieved_to_be_displayed.jobSalary,
                'JobSummary': job_retrieved_to_be_displayed.jobSummary,
            }
            result = jobDetailsCollection.insert_one(Job)

        # Jobs Database is not empty
        else:
            # check if the job already exists or not
            jobsData = jobDetailsCollection.find_one({"JobTitle": job_retrieved_to_be_displayed.jobTitle})

            # If does not exists, retrieve the number of jobs and assign count+1 as jobId
            if jobsData is None:
                no_of_documents = jobDetailsCollection.count();
                jobId = no_of_documents + 1
                Job = {
                    'userassignedId': jobId,
                    'JobTitle': job_retrieved_to_be_displayed.jobTitle,
                    'JobCompany': job_retrieved_to_be_displayed.jobCompany,
                    'JobLocation': job_retrieved_to_be_displayed.jobLocation,
                    'JobSalary': job_retrieved_to_be_displayed.jobSalary,
                    'JobSummary': job_retrieved_to_be_displayed.jobSummary,
                }
                result = jobDetailsCollection.insert_one(Job)
            else:
                jobId = jobsData['userassignedId']

        # If the user has rated the job before
        feed_back_of_user = explicitFbDB.reviews.find_one({"Userid": UserRecord[0].idformongo, "Jobid": jobId})

        # If he hadn't
        if feed_back_of_user is None:
            print("Nothing initially in the DB")
            Feedback = {
                'Userid': UserRecord[0].idformongo,
                'Jobid': jobId,
                'ExplicitRating': Number[1]
            }
            result = explicitFbDB.reviews.insert_one(Feedback)
        #If he had, update the rating
        else:
            explicitFbDB.reviews.update(
                {"Jobid": jobId, "Userid": UserRecord[0].idformongo},
                {"$set": {"ExplicitRating": Number[1]}}
            )
    return render(request, 'jobs.html', {"jobList": jobs})
