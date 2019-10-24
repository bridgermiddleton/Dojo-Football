from django.shortcuts import render, redirect
import bcrypt
import nflgame
from .models import User, Player, TWeek
from .utils import *

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

<<<<<<< HEAD
=======

>>>>>>> c4ab140ddf2071f09812fcc005c1077e7ee46749
def teamHome(request):
    current_user = User.objects.get(id=request.session["userid"])
    roster = current_user.players.all() #list of player objects
    for p in roster:
        p.total_points = score(p.gsis_id, week=2)

    context = {
        "user": current_user,
        "roster": roster
    }
    return render(request, "football_app/teamHome.html", context)

def filterStatus(theplayer):
    if theplayer.status == "ACT":
        return True
    else:
        return False

<<<<<<< HEAD
def home(request):
    teams = User.objects.order_by("W")
    weeks = User.objects.order_by("id")
    theweek=         {
        'week1' : [weeks[4],weeks[2],weeks[8],weeks[5],weeks[6],weeks[1],weeks[7],weeks[3],weeks[0],weeks[9]],
        'week2' : [weeks[4],weeks[5],weeks[8],weeks[9],weeks[1],weeks[2],weeks[6],weeks[3],weeks[7],weeks[0]],
        'week3' : [weeks[4],weeks[8],weeks[1],weeks[5],weeks[3],weeks[2],weeks[6],weeks[0],weeks[7],weeks[9]],
        'week4' : [weeks[4],weeks[9],weeks[3],weeks[5],weeks[1],weeks[8],weeks[0],weeks[2],weeks[6],weeks[7]],
        'week5' : [weeks[4],weeks[1],weeks[0],weeks[5],weeks[3],weeks[8],weeks[7],weeks[2],weeks[6],weeks[9]],
        'week6' : [weeks[4],weeks[3],weeks[7],weeks[5],weeks[0],weeks[8],weeks[1],weeks[9],weeks[6],weeks[2]],
        'week7' : [weeks[4],weeks[0],weeks[6],weeks[5],weeks[7],weeks[8],weeks[3],weeks[1],weeks[9],weeks[2]],
        'week8' : [weeks[4],weeks[7],weeks[6],weeks[8],weeks[0],weeks[1],weeks[2],weeks[5],weeks[3],weeks[9]],
    }
    print(weeks[0])
    context = {
        'teams' : teams,
        'length' : range(1,len(teams)+1),
        'superlength' : len(teams),
        'weeks' : theweek['week1']
    }
    return render(request, "football_app/user_home.html", context)
=======
>>>>>>> c4ab140ddf2071f09812fcc005c1077e7ee46749
def draftpage(request):
    if 'userid' in request.session:
        print("#"*80)
        current_user = User.objects.get(id=request.session['userid'])
        roster = Player.objects.filter(user=current_user)
        if len(roster)<7:
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

<<<<<<< HEAD
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
=======
                

            context = {
                "all_players": available_players,
            }

            return render(request, "football_app/draftpage.html", context)
        else: 
            return redirect("/teamHome")
>>>>>>> c4ab140ddf2071f09812fcc005c1077e7ee46749
    else:
        return redirect("/")
def matchup(request):
    return render(request, "football_app/matchup_page.html")
def homeWeek(request, val):
    teams = User.objects.order_by("W")
    weeks = User.objects.order_by("id")
    weekDisplay = 'Week '+str(val)
    theweek=         {
        'week1' : [weeks[4],weeks[2],weeks[8],weeks[5],weeks[6],weeks[1],weeks[7],weeks[3],weeks[0],weeks[9]],
        'week2' : [weeks[4],weeks[5],weeks[8],weeks[9],weeks[1],weeks[2],weeks[6],weeks[3],weeks[7],weeks[0]],
        'week3' : [weeks[4],weeks[8],weeks[1],weeks[5],weeks[3],weeks[2],weeks[6],weeks[0],weeks[7],weeks[9]],
        'week4' : [weeks[4],weeks[9],weeks[3],weeks[5],weeks[1],weeks[8],weeks[0],weeks[2],weeks[6],weeks[7]],
        'week5' : [weeks[4],weeks[1],weeks[0],weeks[5],weeks[3],weeks[8],weeks[7],weeks[2],weeks[6],weeks[9]],
        'week6' : [weeks[4],weeks[3],weeks[7],weeks[5],weeks[0],weeks[8],weeks[1],weeks[9],weeks[6],weeks[2]],
        'week7' : [weeks[4],weeks[0],weeks[6],weeks[5],weeks[7],weeks[8],weeks[3],weeks[1],weeks[9],weeks[2]],
        'week8' : [weeks[4],weeks[7],weeks[6],weeks[8],weeks[0],weeks[1],weeks[2],weeks[5],weeks[3],weeks[9]],
    }
    val='week'+str(val)
    thisWeek = theweek[val]
    context = {
        'teams' : teams,
        'length' : range(1,len(teams)+1),
        'superlength' : len(teams),
        'weeks' : thisWeek,
        'weekDisplay' : weekDisplay
    }
    return render(request, "football_app/user_home.html", context)
def draftplayer(request):
    all_players = list(nflgame.players.values())
    active_players = list(filter(filterStatus, all_players))
    user = User.objects.get(id=request.session['userid'])
    for a in active_players:
        if a.gsis_id == request.POST['player']:
            thisP = a
    newPlayer = Player.objects.create(first_name = thisP.first_name, last_name = thisP.last_name, gsis_id =thisP.gsis_id, position = thisP.position, total_points=0, passing_yards=0, rushing_yards=0, receiving_yards=0, passing_tds=0, rushing_tds=0, receiving_tds=0, receptions=0, user=user)
    print(newPlayer)
    return redirect("/draftpage")

