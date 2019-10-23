from django.shortcuts import render, redirect
import bcrypt
from .models import *
import nflgame

def loginpage(request):
    return render(request, "football_app/loginpage.html")


def registerpage(request):
    return render(request, "football_app/registerpage.html")

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            redirect('/home')
    else:
        return redirect("/")

def register(request):
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=pw_hash.decode(),team_name=request.POST['team_name'],W=0,L=0)
    request.session['userid'] = user.id
    return redirect('/home')

def logout(request):
   if 'userid' in request.session:
       del request.session['userid']
   return redirect("/")

def filterStatus(theplayer):
    if theplayer.status == "ACT":
        return True
    else:
        return False

def home(request):
    teams = User.objects.order_by("W")
    context = {
        'teams' : teams,
        'length' : range(1,len(teams)+1),
        'superlength' : len(teams),
    }
    return render(request, "football_app/user_home.html", context)
def draftpage(request):
    if 'userid' in request.session:

        all_players = list(nflgame.players.values())
        active_players = list(filter(filterStatus, all_players))
        all_player_classes = Player.objects.all()
        available_players = []
        for player in active_players:
            taken = False
            for taken_player in all_player_classes:
                if player.gsis_id == taken_player.gsis_id:
                    taken = True
                    break
            if taken == False:
                available_players.append(player)
            context = {
            "all_players": available_players,
        }
        return render(request, "football_app/draftpage.html", context)
    else:
        return redirect("/")
def matchup(request):
    return render(request, "football_app/matchup_page.html")