from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loginpage),
    url(r'^registerpage$', views.registerpage),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^draftpage$', views.draftpage),
    url(r'^draftplayer$', views.draftplayer),
    url(r'^teamHome$', views.teamHome)
]