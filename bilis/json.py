import json
import datetime
import MySQLdb
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.html import escape
from django.views.decorators.cache import cache_page
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
        item['datetime'] = game.datetime.strftime("%d.%m.%y %H:%M")
        item['winner'] = "<a href='/player/" + str(game.winner.pk) + "/' >" + escape(game.winner.name) + "</a>" + (" <img src='{{ static  }}'>" if game.under_table else "")
        item['loser'] =  "<a href='/player/" + str(game.loser.pk) + "/' >" + escape(game.loser.name) + "</a>"
        rows.append(item)
    total = Game.objects.count()
    struct['total'] = total
    struct['rows'] = rows
    return HttpResponse(json.dumps(struct, sort_keys=True,
                        indent=4, separators=(',', ': ')), content_type='application/json')

def players(request):
    if request.session.get('rating_type', 'elo') == 'fargo':
        rating_type = 'fargo'
    else:
        rating_type = 'elo'
    #sijoitus, nimi, pisteet, pelatut, voitetut, hävityt
    offset = int(request.GET.get('offset'))
    limit = int(request.GET.get('limit'))
    search = request.GET.get('search')
    sort = request.GET.get('sort')
    order = request.GET.get('order')
    if(sort=='name'):
        sort='last_name'
    if(sort=='rating'):
        sort=rating_type
    if(sort is None):
        sort = '-fargo'
    else:
        sort = MySQLdb.escape_string(sort)
    if(search is None):
        players = Player.objects.raw("select x.id, (select count(*)+1 from bilis_player as t where t.{}>x.{}) as position from bilis_player as x order by {} {}".format(rating_type, rating_type, sort, order))[offset:offset+limit] #TODO: fiksaa
    else:
        search = MySQLdb.escape_string(search)
        players = Player.objects.raw("select x.id, (select count(*)+1 from bilis_player as t where t.{}>x.{}) as position from bilis_player as x where first_name like %s or last_name like %s order by {} {}".format(rating_type, rating_type, sort, order), ['%'+search+'%', '%'+search+'%'])[offset:offset+limit]

    struct = {}
    rows = []
    for i,player in enumerate(players):
        item = {}
        item['position'] = player.position
        item['name'] = "<a href='/player/" + str(player.pk) + "/' >" + escape(player.name) + "</a>"
        item['rating'] = str(player.get_rating(rating_type)) #TODO: ei kovakoodaa
        item['games'] = len(player.games)
        item['won_games'] = player.won_games.count()
        item['lost_games'] = player.lost_games.count()
        rows.append(item)
    total = Player.objects.count()
    struct['total'] = total
    struct['rows'] = rows
    return HttpResponse(json.dumps(struct, sort_keys=True,
                        indent=4, separators=(',',': ')), content_type='application/json')


def rating_time_series(request, player):
    if request.session.get('rating_type', 'elo') == 'fargo':
        rating_type = 'fargo'
    else:
        rating_type = 'elo'
    player = get_object_or_404(Player, pk=player)
    data = cache.get('{}_series_'.format(rating_type) + str(player.pk))
    if data is None:
      data = []
      for i, game in enumerate(reversed(player.games)): #this is a bit hacky, should rethink the API
          point = {}
          point['x'] = i
          point['y'] = float(game.get_winner_rating(rating_type)) if game.winner==player else float(game.get_loser_rating(rating_type))
          data.append(point)
      data.append({'x': len(player.games), 'y': float(player.get_rating(rating_type))})
      cache.set('{}_series_'.format(rating_type) + str(player.pk), data, timeout=None)
    return HttpResponse(json.dumps(data, indent=4, sort_keys=True, separators=(',', ': ')), content_type='application/json')

    
    
