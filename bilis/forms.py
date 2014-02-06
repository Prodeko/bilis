from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from bilis.models import Player

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['name']
        labels = {
            'name': _('Nimi'),
        }
