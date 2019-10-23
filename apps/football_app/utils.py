import nflgame


def score(gsis_id, week):
    for key in nflgame.players:
        if nflgame.players[key].gsis_id==gsis_id:
            # print("found player w matchig gsis_id", str(nflgame.players[key]))
            stats = nflgame.players[key].stats(2019, week).stats
            print(nflgame.players[key].first_name, stats)
            break
    if 'receiving_yds' in stats: #rec yards
        recYdPts = stats['receiving_yds']* .1
    else:
        recYdPts = 0
    if 'rushing_yds' in stats: #rush yards
        rushYdPts = stats['rushing_yds']* .1
    else:
        rushYdPts = 0
    if 'passing_yds' in stats: #pass yards
        passYdPts = stats['passing_yds']* .04
    else:
        passYdPts = 0
    if 'receiving_tds' in stats: #rec TDs
        recTdPts = stats['receiving_tds']* 6
    else:
        recTdPts = 0
    if 'rushing_tds' in stats: #rush TDs
        rushTdPts = stats['rushing_tds']* 6
    else:
        rushTdPts = 0
    if 'passing_tds' in stats: #pass TDs
        passTdPts = stats['passing_tds']* 4
    else:
        passTdPts = 0
    if 'receiving_rec' in stats: #PPR
        recPts = stats['receiving_rec']
    else:
        recPts = 0

    totalPlayerScore = rushYdPts + recYdPts + passYdPts + rushTdPts + recTdPts + passTdPts + recPts

    #return object of these
    print("totalPlayerScore", totalPlayerScore)
    return totalPlayerScore

# OrderedDict([('receiving_rec', 1),
#     ('receiving_yds', 25),
#     ('receiving_tds', 1),
#     ('receiving_lng', 25),
#     ('receiving_lngtd', 25),
#     ('receiving_twopta', 0),
#     ('receiving_twoptm', 0)])

# OrderedDict([('passing_att', 31), 
# ('passing_cmp', 25), 
# ('passing_yds', 429), 
# ('passing_tds', 5), 
# ('passing_ints', 0), 
# ('passing_twopta', 0), 
# ('passing_twoptm', 0), 
# ('rushing_att', 2), 
# ('rushing_yds', 6), 
# ('rushing_tds', 1), 
# ('rushing_lng', 3), 
# ('rushing_lngtd', 3), 
# ('rushing_twopta', 0), 
# ('rushing_twoptm', 0)])