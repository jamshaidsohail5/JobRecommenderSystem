from django.conf.urls import url, include
from django.contrib import admin
from home import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^jobs/', include('jobs.urls')),
    url(r'^$', views.home, name="home"),
]


