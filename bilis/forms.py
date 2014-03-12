#coding: utf8
from django.forms import ModelForm, TextInput, Select
from django.utils.translation import ugettext_lazy as _
from bilis.models import Player, Game

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['name']
        labels = {
            'name': _('Nimi'),
        }
        widgets = {
            'name': TextInput(attrs={'class': u'form-control'})
        }


class ResultForm(ModelForm):
    class Meta:
        model = Game
        fields = ['winner', 'loser', 'under_table']
        labels = {
            'winner': _(u'Voittaja'),
            'loser': _(u'Häviäjä'),
            'under_table': _(u'Pöydän alle'),
        }
        widgets = {
            'winner': Select(attrs={'id': u'winner'}),
            'loser': Select(attrs={'id': u'loser'})
        }
