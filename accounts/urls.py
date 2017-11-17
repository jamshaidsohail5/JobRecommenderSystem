from django.conf.urls import url, include
from accounts import views

app_name = 'accounts'

urlpatterns = [
    url(r'^signup/', views.signup , name="signup"),
    url(r'^login/', views.loginview, name="login"),
    url(r'^logout/', views.logoutview, name="logout"),
]