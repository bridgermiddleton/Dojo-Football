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
    url(r'^teamHome$', views.teamHome),
    url(r'^individualplayerpage/(?P<playerid>\d+)/(?P<week>\d+)$', views.individualplayerpage),
    url(r'^week/(?P<week>\d+)/(?P<playerid>\d+)$', views.eachweekstats),
    url(r'^home$', views.home),
    url(r'^home/(?P<val>[1-8]{1})$', views.homeWeek),
    url(r'^matchup/(?P<val>[1-8]{1})/(?P<match>[0-4]{1})$', views.matchup),
    url(r'^leagueRosters$', views.leagueRosters),
    url(r'^clearUsers$', views.clearUsers)
]