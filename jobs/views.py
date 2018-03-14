import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from pymongo import MongoClient

import sys
import os
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.ml.feature import HashingTF, IDF, Normalizer, StopWordsRemover, RegexTokenizer, Word2Vec
from pyspark.ml.feature import BucketedRandomProjectionLSH
from pyspark.ml.linalg import Vectors
from pyspark.sql.functions import col
import pyspark.sql.functions as psf
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import spatial
from operator import attrgetter
from pyspark.mllib.linalg.distributed import IndexedRow, IndexedRowMatrix


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
    # jobId
    if request.method == "POST":
        global jobs
        client = MongoClient(port=27017)
        db = client.ImplicitFeedback
        db1 = client.Jobs

        # Here i will first get the Job id from the Hidden Text Box
        JobID = [key for key in request.POST if key.startswith("jobId")]

        print(JobID)

        # Getting the username
        username = request.user.username

        # Getting the JobTitle
        Number = JobID[0].split("+")
        print("Job id is ", Number[1])

        job_retrieved_to_be_displayed = jobs[int(Number[1]) - 1]

        # Select * from jobsData where jobtitle = passedParameter

        # Checking if the Job already exists in DB or not
        # If the job do not exist in Db then saving it in the DB

        jobsData = db1.jobsData.find({"JobTitle": job_retrieved_to_be_displayed.jobTitle}, {"userassignedId": 1,
                                                                                            "JobCompany": 1,
                                                                                            "JobLocation": 1,
                                                                                            "JobSalary": 1,
                                                                                            "JobSummary": 1})

        if jobsData.count() == 0:
            print("It came inside")
            Job = {
                'userassignedId': job_retrieved_to_be_displayed.id,
                'JobTitle': job_retrieved_to_be_displayed.jobTitle,
                'JobCompany': job_retrieved_to_be_displayed.jobCompany,
                'JobLocation': job_retrieved_to_be_displayed.jobLocation,
                'JobSalary': job_retrieved_to_be_displayed.jobSalary,
                'JobSummary': job_retrieved_to_be_displayed.jobSummary,
            }
            result = db1.jobsDetail.insert_one(Job)

        feed_back_of_user = db.reviews.find({"Username": username}, {"Username": 1, "JobTitle": 1, "ImplicitRating": 1})

        if feed_back_of_user.count() == 0:
            print("Nothing initially in the DB")
            implicit_feedback_count = 1
            Feedback = {
                'Username': username,
                'JobTitle': job_retrieved_to_be_displayed.jobTitle,
                'ImplicitRating': implicit_feedback_count
            }
            result = db.reviews.insert_one(Feedback)
        else:
            flag = False

            for doc in feed_back_of_user:
                if doc['JobTitle'] == job_retrieved_to_be_displayed.jobTitle:
                    flag = True
                    # This means that the User has already opened this job and gave implplicit rating
                    # So increasing the previous count Would do the job
                    # Incrementing the Job Implicit Rating
                    db.reviews.update(
                        {'Username': username, 'JobTitle': job_retrieved_to_be_displayed.jobTitle},
                        {
                            "$inc": {"ImplicitRating": 1}
                        }
                    )

            if flag == False:
                # This means the User didnt gave any rating to the same job before
                Feedback = {
                    'Username': username,
                    'JobTitle': job_retrieved_to_be_displayed.jobTitle,
                    'ImplicitRating': 1
                }
                result = db.reviews.insert_one(Feedback)

        return render(request, 'jobsDetail.html', {"jobsDetail": job_retrieved_to_be_displayed})


def jobsretrieving(request):
    print("ab to ayaa")
    if request.method == "POST":
        print("aya zaroor")

        global jobs

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
                    jobApplyLink = jobApplyLink.get("href")

                    jobLink_temp = jobApplyLink

                    jobSummary = jobSoup.find("span", {"class": "summary"})
                    if jobSummary:
                        jobData = jobData + " " + jobSummary.text
                        jobSummary_temp = jobSummary.text

                        # print(jobSummary_temp)

                    j += 1
                    jobs.append(Jobs(id_temp, jobTitle_temp, jobCompany_temp, jobLocation_temp, jobSalary_temp,
                                     jobSummary_temp, jobLink_temp))
        return render(request, 'jobs.html', {"jobList": jobs})

    else:
        return render(request, 'jobs.html')


        # if (request.method == "POST"):
        #     salary = ""
        #     summary = ""
        #
        #     keyword = request.POST['keyword']
        #     location = request.POST['location']
        #
        #     print('4')
        #
        #     r = requests.get("https://www.indeed.com/jobs?q=" + keyword + "&l=" + location,
        #                      proxies={"http": "http://35.196.26.166:3128"})
        #     data = r.text
        #     soup = BeautifulSoup(data, 'lxml')
        #     soup = soup.findAll("a", {"class": "turnstileLink"})
        #     j = 1
        #     global jobs
        #     for link in soup:
        #         jobLink = link.get("href")
        #         if "clk" in jobLink:
        #
        #             id = j
        #
        #             jobRequest = requests.get("https://www.indeed.com" + jobLink,
        #                                       proxies={"http": "http://35.196.26.166:3128"})
        #             jobData = jobRequest.text
        #             jobSoup = BeautifulSoup(jobData, 'lxml')
        #
        #             jobTitle = jobSoup.find("b", {"class": "jobtitle"})
        #
        #             title = jobTitle.text
        #             company = ""
        #             jobCompany = jobSoup.find("span", {"class": "company"})
        #             if jobCompany:
        #                 company = jobCompany.text
        #
        #             jobLocation = jobSoup.find("span", {"class": "location"})
        #
        #             if jobLocation:
        #                 location = jobLocation.text
        #
        #             jobSalary = jobSoup.find("span", {"class": "no-wrap"})
        #
        #             if jobSalary:
        #                 salary = jobSalary.text.lstrip()
        #
        #             jobSummary = jobSoup.find("span", {"class": "summary"})
        #
        #             if jobSummary:
        #                 summary = jobSummary.text
        #                 # db.Jobs.update(
        #                 #     {"ID": j},
        #                 #     {"$set": {"Summary": jobSummary.text}}
        #                 # )
        #             j += 1
        #             jobs.append(Jobs(id, title, company, location, salary, summary))
        #
        #         if j == 4:
        #             break
        #
        #     return render(request, 'jobs.html', {"jobList": jobs})
        # else:
        #     return render(request, 'jobs.html')


def saveExplicitRating(request):
    if request.method == "POST":
        global jobs
        client = MongoClient(port=27017)
        db = client.ExplicitFeedback
        actual_star_number_and_job_number = [key for key in request.POST if key.startswith("star")]

        # Getting the username
        username = request.user.username

        print(actual_star_number_and_job_number)

        # Getting the JobTitle
        Number = actual_star_number_and_job_number[0].split("+")
        print("Star Rating is", Number[1])
        print("Job id is ", Number[2])
        if int(Number[2]) != 0:
            job_retrieved_to_be_displayed = jobs[int(Number[2]) - 1]
        else:
            job_retrieved_to_be_displayed = jobs[int(Number[2])]

        feed_back_of_user = db.reviews.find({"Username": username}, {"Username": 1, "JobTitle": 1, "ImplicitRating": 1})

        if feed_back_of_user.count() == 0:
            print("Nothing initially in the DB")
            implicit_feedback_count = 1
            Feedback = {
                'Username': username,
                'JobTitle': job_retrieved_to_be_displayed.jobTitle,
                'ImplicitRating': implicit_feedback_count
            }
            result = db.reviews.insert_one(Feedback)
        else:
            flag = False

            for doc in feed_back_of_user:
                if doc['JobTitle'] == job_retrieved_to_be_displayed.jobTitle:
                    flag = True
                    # This means that the User has already opened this job and gave implplicit rating
                    # So increasing the previous count Would do the job
                    # Incrementing the Job Implicit Rating
                    db.reviews.update(
                        {'Username': username, 'JobTitle': job_retrieved_to_be_displayed.jobTitle},
                        {
                            "$inc": {"ImplicitRating": 1}
                        }
                    )

            if flag == False:
                # This means the User didnt gave any rating to the same job before
                Feedback = {
                    'Username': username,
                    'JobTitle': job_retrieved_to_be_displayed.jobTitle,
                    'ImplicitRating': 1
                }
                result = db.reviews.insert_one(Feedback)

    return render(request, 'jobs.html')




def configureSpark(spark_home=None, pyspark_python=None):
    os.environ['HADOOP_HOME'] = "C:/opt/spark-2.2.1-bin-hadoop2.7/Hadoop/"
    spark_home = "C:/opt/spark-2.2.1-bin-hadoop2.7/"
    os.environ['SPARK_HOME'] = spark_home

    # Add the PySpark directories to the Python path:
    sys.path.insert(1, os.path.join(spark_home, 'python'))
    sys.path.insert(1, os.path.join(spark_home, 'python', 'pyspark'))
    sys.path.insert(1, os.path.join(spark_home, 'python', 'build'))

    # If PySpark isn't specified, use currently running Python binary:
    pyspark_python = pyspark_python or sys.executable
    os.environ['PYSPARK_PYTHON'] = pyspark_python
    os.environ["PYSPARK_SUBMIT_ARGS"] = (
        "--packages org.mongodb.spark:mongo-spark-connector_2.11:2.2.0 pyspark-shell")

def recommendjobs(request):
    configureSpark()
    conf = SparkConf()
    conf.setMaster("local")
    conf.setAppName("spark_wc")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    jobDataFrame = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri",
                                                                                        "mongodb://localhost:27017/JobDatabase.Jobs").load()
    resumeDataFrame = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri",
                                                                                           "mongodb://localhost:27017/ResumeDatabase.Person").load()

    regexJobTokenizer = RegexTokenizer(inputCol="Job Data", outputCol="words", pattern="\\W")
    regexResumeTokenizer = RegexTokenizer(inputCol="Profile Data", outputCol="words", pattern="\\W")

    tokenizedJobDataFrame = regexJobTokenizer.transform(jobDataFrame)
    tokenizedResumeDataFrame = regexResumeTokenizer.transform(resumeDataFrame)

    remover = StopWordsRemover(inputCol="words", outputCol="filtered")

    processedJobDataFrame = remover.transform(tokenizedJobDataFrame)
    processedResumeDataFrame = remover.transform(tokenizedResumeDataFrame)

    processedJobDataFrame = processedJobDataFrame.select("ID", "filtered")
    processedResumeDataFrame = processedResumeDataFrame.select("ID", "filtered")

    hashingTF = HashingTF(inputCol="filtered", outputCol="rawFeatures", numFeatures=20)
    featurizedJobDataFrame = hashingTF.transform(processedJobDataFrame)
    featurizedResumeDataFrame = hashingTF.transform(processedResumeDataFrame)
    featurizedJobDataFrame.show(truncate=False)
    featurizedResumeDataFrame.show(truncate=False)

    idf = IDF(inputCol="rawFeatures", outputCol="features")
    idfJobModel = idf.fit(featurizedJobDataFrame)
    idfResumeModel = idf.fit(featurizedResumeDataFrame)

    rescaledJobData = idfJobModel.transform(featurizedJobDataFrame)
    rescaledResumeData = idfResumeModel.transform(featurizedResumeDataFrame)

    normalizer = Normalizer(inputCol="features", outputCol="norm")
    dataJ = normalizer.transform(rescaledJobData)
    dataR = normalizer.transform(rescaledResumeData)

    dot_udf = psf.udf(lambda x, y: float(x.dot(y)))
    SimilarityDataFrame = dataR.alias("Resume").crossJoin(dataJ.alias("Job")) \
        .select(
        psf.col("Resume.ID").alias("ResumeID"),
        psf.col("Job.ID").alias("JobID"),
        dot_udf("Resume.norm", "Job.norm").alias("Cosine Similarity")) \
        .sort("ResumeID", "JobID")

    ResumeOneRecommendations = SimilarityDataFrame.where(SimilarityDataFrame.ResumeID == '1')
    OrderedResumeOneRecommendations = ResumeOneRecommendations.sort("Cosine Similarity", ascending=False).collect()
    i = 0
    for x in OrderedResumeOneRecommendations:
        print(x)
        if i is 5:
            break
        i += 1



    return render(request, 'jobs.html')




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
