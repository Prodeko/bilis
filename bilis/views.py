from django.shortcuts import render_to_response, redirect, render
from django.forms import ModelForm
from django.template import RequestContext
from bilis.models import Player
from bilis.forms import PlayerForm

def index(request):
    return render_to_response('base.html')

def add_player(request):
    if request.method == 'POST':
        print "foo"
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bilis.views.index')
    else:
        form = PlayerForm()
    return render_to_response('add_player.html',{
                'form': form,
        }, context_instance=RequestContext(request))
