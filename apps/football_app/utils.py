import nflgame

def score(gsis_id, week):
    rushYd = weeklyRushYds* .1
    recYd = weeklyRecYds * .1
    passYd = weeklyPassYds * .04
    rushTd = weeklyRushTd * 6
    recTd = weeklyRecTd * 6
    passTd = weeklyPassTd *  4
    rec = weeklyRecYds * 1
    print("this is working")
    return rushYd, recYd, passYd, rushTd, recTd, passTd, rec
