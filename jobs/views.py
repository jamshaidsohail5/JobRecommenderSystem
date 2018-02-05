from django.shortcuts import render
from datetime import datetime
from careerjet_api_client import CareerjetAPIClient
from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
import re


class Jobs(object):
    # Note that we're taking an argument besides self, here.
    def __init__(self,id = 0,jobTitle = "",jobCompany = "",jobLocation = "",jobSalary = "",jobSummary = ""):
        self.id = id  # Set the room's name to the name we got.
        self.jobTitle = jobTitle
        self.jobCompany = jobCompany
        self.jobLocation = jobLocation
        self.jobSalary = jobSalary
        self.jobSummary = jobSummary



def jobsviewing(request):
    return render(request, 'jobs.html')


def jobsretrieving(request):
    # print("1")
    # cj = CareerjetAPIClient("en_GB");
    # print('2')

    if (request.method == "POST"):
        print('3')
        keyword = request.POST['keyword']
        location = request.POST['location']

        print('4')

        #keyword = 'python'
        #location = 'lahore'

        #client = MongoClient('localhost:27017')
        #db = client.JobDatabase

        #desc = "web"
        #loc = "lahore"
        r = requests.get("https://www.indeed.com/jobs?q=" + keyword + "&l=" + location,
                         proxies={"http": "http://61.233.25.166:80"})
        data = r.text
        soup = BeautifulSoup(data, 'lxml')
        soup = soup.findAll("a", {"class": "turnstileLink"})
        j = 1
        jobs = []
        id = 0

        title = ""
        salary = ""
        location = ""
        summary = ""
        company = ""
        for link in soup:
            jobLink = link.get("href")
            if "clk" in jobLink:
                # db.Jobs.insert_one(
                #     {
                #         "ID": j,
                #     })
                print ("ID :",j)
                id = j


                jobRequest = requests.get("https://www.indeed.com" + jobLink,
                                          proxies={"http": "http://61.233.25.166:80"})
                jobData = jobRequest.text
                jobSoup = BeautifulSoup(jobData, 'lxml')

                jobTitle = jobSoup.find("b", {"class": "jobtitle"})

                # db.Jobs.update(
                #     {"ID": j},
                #     {"$set": {"Title": jobTitle.text}}
                # )
                print("Title:",jobTitle.text)

                title = jobTitle.text




                jobCompany = jobSoup.find("span", {"class": "company"})
                if jobCompany:
                    company = jobCompany.text
                    print("Company:",jobCompany.text)
                    # db.Jobs.update(
                    #     {"ID": j},
                    #     {"$set": {"Company": jobCompany.text}}
                    # )



                jobLocation = jobSoup.find("span", {"class": "location"})
                if jobLocation:
                    location = jobLocation.text
                    print("Location:",jobLocation.text)
                    # db.Jobs.update(
                    #     {"ID": j},
                    #     {"$set": {"Location": jobLocation.text}}
                    # )


                jobSalary = jobSoup.find("span", {"class": "no-wrap"})

                if jobSalary:
                    salary = jobSalary.text.lstrip()
                    # db.Jobs.update(
                    #     {"ID": j},
                    #     {"$set": {"Salary": jobSalary.text}}
                    # )
                    print("Salary:",jobSalary.text.lstrip())

                jobSummary = jobSoup.find("span", {"class": "summary"})
                if jobSummary:
                    summary = jobSummary.text.encode('utf-8')
                    print("Summary:",jobSummary.text.encode('utf-8'))
                    # db.Jobs.update(
                    #     {"ID": j},
                    #     {"$set": {"Summary": jobSummary.text}}
                    # )
                j += 1
                jobs.append(Jobs(id,title,company,location,salary,summary))

            if j == 4:
                break

        return render(request, 'jobs.html', {"jobList": jobs})









                # result_json = cj.search({
                #     'location': location,
                #     'keywords': keyword,
                #     'affid': '213e213hd12344552',
                #     'user_ip': '11.22.33.44',
                #     'url': 'http://www.example.com/jobsearch?q=python&l=london',
                #     'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
                # });
                # print('5')
                #
                #
                # now = datetime.now()
                # print('6')
                #
                # for job in result_json["jobs"]:
                #     jobPosted = job["date"]
                #     jobPosted = datetime.strptime(jobPosted, '%a, %d %b %Y %H:%M:%S %Z')
                #     job["dayMonth"] = str(jobPosted.strftime('%b %d'))
                #     if abs((now - jobPosted).days) == 1:
                #         job["date"] = str(abs((now - jobPosted).days)) + " day"
                #     elif abs((now - jobPosted).days) == 0:
                #         job["date"] = str(abs((now - jobPosted).seconds) / 3600) + " hours"
                #     else:
                #         job["date"] = str(abs((now - jobPosted).days)) + " days"
                #         print("7")
                #
                # print("8")
                # i = 0;
                # for job in result_json["jobs"]:
                #     job["description"] = job["description"].replace('</b>', '').replace('<b>', '').split()
                #     job["id"] = i
                #     i = i + 1

