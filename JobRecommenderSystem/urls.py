from django.conf.urls import url, include
from django.contrib import admin
from JobRecommenderSystem import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^mainpage/', include('jobs.urls')),
    url(r'^home/',include('home.urls')),
    url(r'^$', views.home, name="home"),
]


