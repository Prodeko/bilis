from django.forms import ModelForm, TextInput
from django.utils.translation import ugettext_lazy as _
from bilis.models import Player, Game

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['name']
        labels = {
            'name': _('Nimi'),
        }
class ResultForm(ModelForm):
    class Meta:
        model = Game
        fields = ['winner', 'loser']
        widgets = {
            'winner': TextInput(attrs={'class': u'form-control'}),
            'loser': TextInput(attrs={'class': u'form-control'})
            }
