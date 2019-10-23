from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.loginpage),
    url(r'^registerpage$', views.registerpage),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^home$', views.home),
    url(r'^draftpage$', views.draftpage),
    url(r'^matchup$', views.matchup),
    url(r'^logout$', views.logout)

]