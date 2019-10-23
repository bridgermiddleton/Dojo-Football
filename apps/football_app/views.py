from django.shortcuts import render, redirect
import bcrypt
import nflgame
from .models import User, Player, TWeek, PWeek

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

def reset(request):
    for user in User.objects.all():
        for player in user.players.all():
            player.delete()
    return redirect("/draftpage")

def userteamhome(request):
    context = {
        "user": User.objects.get(id=request.session['userid']),
        "week": 7
    }
    return render(request, "football_app/userteamhome.html", context)


def individualplayerpage(request, playerid, week):
    weeknumber = int(week)
    context = {
        "player": Player.objects.get(id=playerid),
        "pweek": PWeek.objects.get(player=Player.objects.get(id=playerid),week=weeknumber),
        "week": weeknumber

    }
    return render(request, "football_app/individualplayerpage.html", context)


def getplayerstats(request, playerid, week):
    theplayer = Player.objects.get(id=playerid)
    weeknumber = int(week)

    for key in nflgame.players:
        if nflgame.players[key].gsis_id == theplayer.gsis_id:
            stats = nflgame.players[key].stats(2019, week=weeknumber).stats
            pweek = PWeek.objects.filter(player=Player.objects.get(id=playerid), week=weeknumber)
            if pweek:
                return redirect(f"/individualplayerpage/{playerid}/{week}")
            else:
                if 'passing_yds' in stats:
                    passing_yards = stats['passing_yds']
                else:
                    passing_yards = 0

                if 'rushing_yds' in stats:
                    rushing_yards = stats['rushing_yds']
                else:
                    rushing_yards = 0
                    
                if 'receiving_yds' in stats:
                    receiving_yards = stats['receiving_yds']
                else:
                    receiving_yards = 0
                    
                if 'passing_tds' in stats:
                    passing_tds = stats['passing_tds']
                else:
                    passing_tds = 0
                    
                if 'rushing_tds' in stats:
                    rushing_tds = stats['rushing_tds']
                else:
                    rushing_tds = 0
                if 'receiving_tds' in stats:
                    receiving_tds = stats['receiving_tds']
                else:
                    receiving_tds = 0
                    
                if 'receiving_rec' in stats:
                    receptions = stats['receiving_rec']
                else:
                    receptions = 0
        
                PWeek.objects.create(points=0,passing_yards=passing_yards,rushing_yards=rushing_yards,receiving_yards=receiving_yards,passing_tds=passing_tds,rushing_tds=rushing_tds,receiving_tds=receiving_tds,receptions=receptions,player=Player.objects.get(id=playerid),week=weeknumber)

                return redirect(f"/individualplayerpage/{playerid}/{week}")



def eachweekstats(request, week, playerid):
    weeknumber = int(week)
    context = {
        "player": playerid,
        "pweek": PWeek.objects.get(player=Player.objects.get(id=playerid),week=weeknumber)
    }
    return render(request, "football_app/eachweekstats.html", context)