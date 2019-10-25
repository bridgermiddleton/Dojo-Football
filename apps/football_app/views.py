from django.shortcuts import render, redirect
import bcrypt
import nflgame
from .models import User, Player, TWeek, PWeek
from .utils import *
import requests



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


def teamHome(request):
    current_user = User.objects.get(id=request.session["userid"])
    roster = current_user.players.all() #list of player objects
    total_score = 0
    new_total_score = 0
    current_week = 'http://www.nfl.com/feeds-rs/currentWeek.json'
    current_week = requests.get(current_week)
    current_week = current_week.json()
    current_week = int(current_week['week']) - 1


    for p in roster:
        for pweek in p.weeks.all():
            if pweek.week == current_week:
                new_total_score += pweek.points



    context = {
        "user": current_user,
        "roster": roster,
        "week": current_week,
        "new_total_score": new_total_score
    }
    return render(request, "football_app/teamHome.html", context)

def filterStatus(theplayer):
    if theplayer.status == "ACT":
        return True
    else:
        return False
def draftpage(request):
    if 'userid' in request.session:

        current_user = User.objects.get(id=request.session['userid'])
        roster = Player.objects.filter(user=current_user)
        QBCount = 0
        RBCount = 0
        WRCount = 0
        TECount = 0
        for r in roster:
            if r.position == "QB":
                QBCount += 1
            if r.position == "RB":
                RBCount += 1
            if r.position == "WR":
                WRCount += 1
            if r.position == "TE":
                TECount += 1
        MaxQB = False
        MaxRB = False
        MaxWR = False
        MaxTE = False
        if QBCount == 1:
            MaxQB = True
        if RBCount == 2:
            MaxRB = True
        if WRCount == 3:
            MaxWR = True
        if TECount == 1:
            MaxTE = True
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

            

            context = {
                "all_players": available_players,
                "MaxQB": MaxQB,
                "MaxRB": MaxRB,
                "MaxWR": MaxWR,
                "MaxTE": MaxTE
            }

            return render(request, "football_app/draftpage.html", context)
        else:
            return redirect("/teamHome")
    else:
        return redirect("/")
def draftplayer(request):
    all_players = list(nflgame.players.values())
    active_players = list(filter(filterStatus, all_players))
    user = User.objects.get(id=request.session['userid'])
    current_week = 'http://www.nfl.com/feeds-rs/currentWeek.json'
    current_week = requests.get(current_week)
    current_week = current_week.json()
    current_week = int(current_week['week'])
    for a in active_players:
        if a.gsis_id == request.POST['player']:
            thisP = a
    newPlayer = Player.objects.create(first_name = thisP.first_name, last_name = thisP.last_name, gsis_id =thisP.gsis_id, position = thisP.position, total_points=0, user=user)
    print(newPlayer)
    for i in range(1,current_week,1):
        total_score = 0
        newPlayer.total_points = score(newPlayer.gsis_id, week=i)
        total_score += newPlayer.total_points
        newPlayer.save()

        for key in nflgame.players:
            if nflgame.players[key].gsis_id == newPlayer.gsis_id:
                stats = nflgame.players[key].stats(2019, week=i).stats
                pweek = PWeek.objects.filter(player=newPlayer, week=i)
                if pweek:
                    return redirect(f"/individualplayerpage/{newPlayer.id}/{i}")
                else:
                    print("hello")
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
            
                    PWeek.objects.create(points=newPlayer.total_points,passing_yards=passing_yards,rushing_yards=rushing_yards,receiving_yards=receiving_yards,passing_tds=passing_tds,rushing_tds=rushing_tds,receiving_tds=receiving_tds,receptions=receptions,player=newPlayer,week=i)


    return redirect("/draftpage")

def reset(request):
    for user in User.objects.all():
        for player in user.players.all():
            player.delete()
    return redirect("/draftpage")


def individualplayerpage(request, playerid, week):
    weeknumber = int(week)
    context = {
        "player": Player.objects.get(id=playerid),
        "pweek": PWeek.objects.get(player=Player.objects.get(id=playerid),week=weeknumber),
        "week": weeknumber

    }
    return render(request, "football_app/individualplayerpage.html", context)

def eachweekstats(request, week, playerid):
    weeknumber = int(week)
    context = {
        "player": Player.objects.get(id=playerid),
        "pweek": PWeek.objects.get(player=Player.objects.get(id=playerid),week=weeknumber),
        "week": weeknumber
    }
    return render(request, "football_app/individualplayerpage.html", context)

def home(request):
    teams = User.objects.order_by("W")
    weeks = User.objects.order_by("id")
    current_week = 'http://www.nfl.com/feeds-rs/currentWeek.json'
    current_week = requests.get(current_week)
    current_week = current_week.json()
    current_week = current_week['week']-1
    render_week = 'week' + str(current_week)
    weekDisplay = 'Week '+ str(current_week)
    if len(weeks) == 10:
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
    try:
        context = {
            'teams' : teams,
            'length' : range(1,len(teams)+1),
            'superlength' : len(teams),
            'weeks' : theweek['week1'],
            'matchweek' : current_week
        }
    except:
                context = {
            'teams' : teams,
            'length' : range(1,len(teams)+1),
            'superlength' : len(teams),
            'matchweek' : current_week
        }
    return render(request, "football_app/user_home.html", context)
def homeWeek(request, val):
    teams = User.objects.order_by("W")
    weeks = User.objects.order_by("id")
    weekDisplay = 'Week '+str(val)
    current_week = 'http://www.nfl.com/feeds-rs/currentWeek.json'
    current_week = requests.get(current_week)
    current_week = current_week.json()
    current_week = current_week['week']-1
    render_week = 'week' + str(current_week)
    value='week'+str(val)
    if len(weeks) == 10:
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
            'weekDisplay' : weekDisplay,
            'matchweek' : val
        }
        return render(request, "football_app/user_page.html", context)
    else:
        context = {
            'teams' : teams,
            'length' : range(1,len(teams)+1),
            'superlength' : len(teams),
            'weekDisplay' : weekDisplay,
            'errormessage': '>>Ten Teams Required In Fantasy League',
            'matchweek' : val
        }
        return render(request, "football_app/user_home.html", context)


def matchup(request, val, match):
    weeks = User.objects.order_by("id")
    match = int(match)*2
    weekDisplay = 'Week '+str(val)
    Team1Total = 0
    Team2Total = 0
    
    if len(weeks) == 10:
        theweek =   {
            'week1' : [weeks[8],weeks[5],weeks[6],weeks[1],weeks[4],weeks[2],weeks[7],weeks[3],weeks[0],weeks[9]],
            'week2' : [weeks[4],weeks[5],weeks[8],weeks[9],weeks[1],weeks[2],weeks[6],weeks[3],weeks[7],weeks[0]],
            'week3' : [weeks[1],weeks[5],weeks[4],weeks[8],weeks[3],weeks[2],weeks[6],weeks[0],weeks[7],weeks[9]],
            'week4' : [weeks[4],weeks[9],weeks[3],weeks[5],weeks[1],weeks[8],weeks[0],weeks[2],weeks[6],weeks[7]],
            'week5' : [weeks[4],weeks[1],weeks[0],weeks[5],weeks[3],weeks[8],weeks[7],weeks[2],weeks[6],weeks[9]],
            'week6' : [weeks[7],weeks[5],weeks[0],weeks[8],weeks[1],weeks[9],weeks[6],weeks[2],weeks[4],weeks[3]],
            'week7' : [weeks[4],weeks[0],weeks[6],weeks[5],weeks[7],weeks[8],weeks[3],weeks[1],weeks[9],weeks[2]],
            'week8' : [weeks[6],weeks[8],weeks[0],weeks[1],weeks[2],weeks[5],weeks[4],weeks[7],weeks[3],weeks[9]],
        }
        val='week'+str(val)
        thisWeek = theweek[val]
        win1 = False
        win2 = False
        for u in thisWeek[match].players.all():
            pweek = PWeek.objects.get(week=val,player=u)
            Team1Total += pweek.points
        for u in thisWeek[match+1].players.all():
            pweek = PWeek.objects.get(week=val,player=u)
            Team2Total += pweek.points
        if Team1Total > Team2Total:
            win1 = True
        else:
            win2= True
            context = {
                'weeks' : thisWeek,
                'weekDisplay' : weekDisplay,
                'matchupT1' : thisWeek[match].players.all(),
                'matchupT2' : thisWeek[match+1].players.all(),
                'team1' : thisWeek[match].team_name,
                'team2' : thisWeek[match+1].team_name,
                'Team1Score' : Team1Total,
                'Team2Score' : Team2Total,
            }
        return render(request, "football_app/matchup_page.html", context,theweek)
    else:

        context = {
            'weekDisplay' : weekDisplay,
            'team1' : "Team 1",
            'team2' : "Team 2",
            'win1' : False,
            'win2' : False,
        }
    return render(request, "football_app/matchup_page.html", context)



def leagueRosters(request):
    teams = User.objects.all()
    total_score = 0
    current_week = 'http://www.nfl.com/feeds-rs/currentWeek.json'
    current_week = requests.get(current_week)
    current_week = current_week.json()
    current_week = int(current_week['week']) - 1
    
            

    context = {
        "teams": teams,
        "current_week": current_week

    }
    return render(request, "football_app/leagueRosters.html", context)


def clearUsers(requests):
    for user in User.objects.all():
        user.delete()
    return redirect("/")

# Create your views here.
