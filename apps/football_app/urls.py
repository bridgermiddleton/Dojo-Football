from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loginpage),
    url(r'^registerpage$', views.registerpage),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
<<<<<<< HEAD
    url(r'^home$', views.home),
    url(r'^matchup$', views.matchup),
    url(r'^logout$', views.logout),
    url(r'^home/(?P<val>[1-8]{1})$', views.homeWeek),

]
=======
    url(r'^draftpage$', views.draftpage),
    url(r'^draftplayer$', views.draftplayer),
    url(r'^teamHome$', views.teamHome)
]
>>>>>>> c4ab140ddf2071f09812fcc005c1077e7ee46749
