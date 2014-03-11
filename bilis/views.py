from django.shortcuts import render_to_response, redirect, render
from django.forms import ModelForm
from django.template import RequestContext
from bilis.models import Player, Game
from bilis.forms import PlayerForm, ResultForm

def index(request):
    form = ResultForm()
    players = Player.objects.all().order_by('-live_rating')[:20]
    latest_games = Game.objects.all().order_by('-datetime')[:20]
    return render_to_response('index.html',{
                'form': form,
                'players': players,
                'latest_games' : latest_games
        }, context_instance=RequestContext(request))

def add_result(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('bilis.views.index')

def new_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bilis.views.index')
    else:
        form = PlayerForm()
    return render_to_response('new_player.html',{
                'form': form,
        }, context_instance=RequestContext(request))
