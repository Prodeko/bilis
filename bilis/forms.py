#coding: utf8
from django.forms import ModelForm, TextInput, Select, ValidationError
from django.utils.translation import ugettext_lazy as _
from bilis.models import Player, Game

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': _('Etunimi'),
            'last_name': _('Sukunimi'),
        }
        widgets = {
            'first_name': TextInput(attrs={'class': u'form-control'}),
            'last_name': TextInput(attrs={'class': u'form-control'}),
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
    def clean(self):

        if (self.cleaned_data.get('winner') == self.cleaned_data.get('loser')):
            raise ValidationError(
                "Voittaja ja häviäjä ei voi olla sama pelaaja."
            )

        return self.cleaned_data
