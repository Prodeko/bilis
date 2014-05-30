from django.forms import Form, ModelForm, TextInput, Select, ValidationError, CharField, FileField
from django.utils.translation import ugettext_lazy as _
from bilis.models import Player, Game

class PlayerForm(ModelForm):
    favorite_color_string = CharField(
        widget = TextInput(attrs={'class': 'form-control color{hash:true}',}),
        label = 'Lempiväri',
        initial = '#FF0000',
    )
    class Meta:
        model = Player
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': _('Etunimi'),
            'last_name': _('Sukunimi'),
        }
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
        }


class ResultForm(ModelForm):
    class Meta:
        model = Game
        fields = ['winner', 'loser', 'under_table']
        labels = {
            'winner': _('Voittaja'),
            'loser': _('Häviäjä'),
            'under_table': _('Pöydän alle'),
        }
        widgets = {
            'winner': Select(attrs={'id': u'winner'}),
            'loser': Select(attrs={'id': u'loser'})
        }
        error_messages = {
            'winner': {
                'required': _('Valitse voittaja.'),
            },
            'loser': {
                'required': _('Valitse häviäjä.'),
            },
        }
    def clean(self):
        # winner and loser can't be the same player
        if (self.cleaned_data.get('winner') == self.cleaned_data.get('loser')):
            #only raise this error if the player is not None
            if (self.cleaned_data.get('winner') is not None):
                raise ValidationError(
                    "Voittaja ja häviäjä ei voi olla sama pelaaja."
                )

        return self.cleaned_data
        
class ImageUploadForm(Form):
    image = FileField(allow_empty_file=False)
