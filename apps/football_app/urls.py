from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loginpage),
    url(r'^registerpage$', views.registerpage),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^draftpage$', views.draftpage),
    url(r'^draftplayer$', views.draftplayer),
    url(r'^reset$', views.reset),
    url(r'^userteamhome$', views.userteamhome),
    url(r'^individualplayerpage/(?P<playerid>\d+)$', views.individualplayerpage),
    url(r'^getplayerstats/(?P<playerid>\d+)$', views.getplayerstats)

]