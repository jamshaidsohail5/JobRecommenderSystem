from django.shortcuts import render
from datetime import datetime
from careerjet_api_client import CareerjetAPIClient


def jobsviewing(request):
    return render(request, 'jobs.html')


def jobsretrieving(request):
    print("1")
    cj = CareerjetAPIClient("en_GB");
    print('2')

    if (request.method == "POST"):
        print('3')

        keyword = request.POST['keyword']
        location = request.POST['location']
    else:
        print('4')

        keyword = 'python'
        location = 'lahore'
    result_json = cj.search({
        'location': location,
        'keywords': keyword,
        'affid': '213e213hd12344552',
        'user_ip': '11.22.33.44',
        'url': 'http://www.example.com/jobsearch?q=python&l=london',
        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
    });
    print('5')


    now = datetime.now()
    print('6')

    for job in result_json["jobs"]:
        jobPosted = job["date"]
        jobPosted = datetime.strptime(jobPosted, '%a, %d %b %Y %H:%M:%S %Z')
        job["dayMonth"] = str(jobPosted.strftime('%b %d'))
        if abs((now - jobPosted).days) == 1:
            job["date"] = str(abs((now - jobPosted).days)) + " day"
        elif abs((now - jobPosted).days) == 0:
            job["date"] = str(abs((now - jobPosted).seconds) / 3600) + " hours"
        else:
            job["date"] = str(abs((now - jobPosted).days)) + " days"
            print("7")

    print("8")
    i = 0;
    for job in result_json["jobs"]:
        job["description"] = job["description"].replace('</b>', '').replace('<b>', '').split()
        job["id"] = i
        i = i + 1

    return render(request, 'jobs.html', {"jobList": result_json["jobs"]})
