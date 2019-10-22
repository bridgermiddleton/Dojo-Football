from django.shortcuts import render, redirect
import bcrypt
import nflgame
from .models import User, Player, TWeek

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
            return redirect("/draftpage")
        else:
            return redirect("/")
    else:
        return redirect("/")

def register(request):
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=pw_hash,team_name=request.POST['team_name'],W=0,L=0)
    request.session['userid'] = user.id
    return redirect("/draftpage")

def logout(request):
   if 'userid' in request.session:
       del request.session['userid']
   return redirect("/")
# Create your views here.
def filterStatus(theplayer):
    if theplayer.status == "ACT":
        return True
    else:
        return False
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

