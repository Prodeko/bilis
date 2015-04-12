from django.shortcuts import render_to_response, redirect, render
from django.forms import ModelForm
from django.conf import settings
from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from bilis.models import Player, Game
from bilis.forms import PlayerForm, ResultForm, ImageUploadForm
import json

def index(request):
    form = ResultForm()
    players = Player.objects.all().order_by('-fargo')[:20] #TODO: fix
    latest_games = Game.objects.filter(deleted=False).order_by('-datetime')[:20]
    if Game.objects.count() > 0:
        allow_delete = not Game.objects.latest('datetime').deleted
    else: 
        allow_delete = False
    return render_to_response('index.html',{
                'form': form,
                'players': players,
                'latest_games' : latest_games,
                'allow_delete' : allow_delete
        }, context_instance=RequestContext(request))

def add_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bilis.views.index')
        else:
            players = Player.objects.all().order_by('-fargo')[:20] #TODO: korjaa eri rankingit
            latest_games = Game.objects.all().order_by('-datetime')[:20]
            if Game.objects.count() > 0:
                allow_delete = not Game.objects.latest('datetime').deleted
            else: 
                allow_delete = False
            return render_to_response('index.html',{
                 'form': form,
                 'players': players,
                 'latest_games' : latest_games,
                 'allow_delete' : allow_delete
                 }, context_instance=RequestContext(request))
    return redirect('bilis.views.index')
	
def delete_last_result(request):
    game = Game.objects.latest('datetime')
    game.deleted = True
    game.save()
    game.winner.elo = game.winner_elo
    game.loser.elo = game.loser_elo
    game.winner.fargo = game.winner_fargo
    game.loser.fargo = game.loser_fargo
    game.winner.save()
    game.loser.save()
    return redirect('bilis.views.index')

def new_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.favorite_color = utils.html_color_to_int(form.cleaned_data['favorite_color_string'])
            player.save()
            return redirect('bilis.views.index')
    else:
        form = PlayerForm()
    return render_to_response('new_player.html',{
                'form': form,
        }, context_instance=RequestContext(request))

def delete_player(request, player):
    player = get_object_or_404(Player, pk=player)
    if(len(player.games)==0):
        player.delete()
    return redirect('bilis.views.index')

def players(request):
    players = Player.objects.all().order_by('-fargo')  #TODO: korjaa vaihtoehto
    return render_to_response('players.html',{
                'players': players
        }, context_instance=RequestContext(request))

def player(request, player):
    player = get_object_or_404(Player, pk=player)
    return render_to_response('player.html',{
                'player': player
        }, context_instance=RequestContext(request))

def games(request):
    games = Game.objects.filter(deleted=False).order_by('-datetime')
    return render_to_response('games.html', {
                'games': games
    }, context_instance=RequestContext(request))

def ajax_player_network(request):
    struct = {}
    nodes = []
    links = []
    for player in Player.objects.all().order_by('pk'):
        item = {}
        item['name'] = player.name
        nodes.append(item)
    link_dict = {}
    for game in Game.objects.all():
        winner_id = game.winner.pk
        loser_id = game.loser.pk
        t = (winner_id, loser_id)
        reverse_t = (loser_id, winner_id)
        if t in link_dict:
            link_dict[t] += 1
        elif reverse_t in link_dict:
            link_dict[reverse_t] += 1
        else:
            link_dict[t] = 1
    for link in link_dict:
        source = link[0]
        target = link[1]
        value = link_dict[link]
        item = {}
        item['source']=source
        item['target']=target
        item['value']=value
        links.append(item)
    struct['links'] = links
    struct['nodes'] = nodes
    return HttpResponse(json.dumps(struct, sort_keys=True,
                  indent=4, separators=(',', ': ')), content_type='application/json')

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            #import pdb; pdb.set_trace()
            handle_image(request.FILES['image'])
            call_command('collectstatic', interactive=False)
            return redirect('bilis.views.index')
    else:
        form = ImageUploadForm()
    return render_to_response('file_form.html', {'form': form}, context_instance=RequestContext(request))

def handle_image(file):
    with open(settings.IMAGE_UPLOAD_PATH+'image.jpg', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def chart(request, player):
    player = get_object_or_404(Player, pk=player)
    return render_to_response('rating_chart.html', {
            'player': player
}, context_instance=RequestContext(request))
