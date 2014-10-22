import json
import datetime
from django.http import HttpResponse
from bilis.models import Player, Game

def games(request):
    offset = int(request.GET.get('offset'))
    limit = int(request.GET.get('limit'))
    search = request.GET.get('search')
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if(sort is None):
        sort = '-datetime'
    elif(order=='asc'):
        sort = '-'+sort
    if(search is None):
            games = Game.objects.all().order_by(sort)[offset:offset+limit]
    else:
        won_games = Game.objects.all().filter(winner__first_name__icontains=search) | Game.objects.all().filter(winner__last_name__icontains=search)
        lost_games = Game.objects.all().filter(loser__first_name__icontains=search) | Game.objects.all().filter(loser__last_name__icontains=search)
        games = (won_games | lost_games).order_by(sort)[offset:offset+limit]
    if(search is not None):
        games = games.filter()
    struct = {}
    rows = []
    for game in games:
        item = {}
        item['datetime'] = game.datetime.strftime("%d.%m.%y %H:%m")
        item['winner'] = game.winner.name
        item['loser'] = game.loser.name
        rows.append(item)
    total = Game.objects.count()
    struct['total'] = total
    struct['rows'] = rows
    return HttpResponse(json.dumps(struct, sort_keys=True,
                        indent=4, separators=(',', ': ')), content_type='application/json')

def players(request):
    #sijoitus, nimi, pisteet, pelatut, voitetut, hävityt
    players = Player.objects.all()
    rows = []
    for i,player in enumerate(players):
        item = {}
        item['position'] = i+1
        item['name'] = player.name
        item['rating'] = str(player.elo)
        item['games'] = len(player.games)
        item['won_games'] = player.won_games.count()
        item['lost_games'] = player.lost_games.count()
        rows.append(item)
    total = players.count()
    print(rows)
    return HttpResponse(json.dumps(rows, sort_keys=True,
                        indent=4, separators=(',',': ')), content_type='application/json')
