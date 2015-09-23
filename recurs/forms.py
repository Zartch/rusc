from django import forms
import autocomplete_light
from etiqueta.models import Etiqueta
from recurs.models import Recurs
from cela.models import get_cela

autocomplete_light.register(Etiqueta, search_fields=('nom', ))

class RecursForm(forms.Form):
    """
    Form for individual user links
    """
    descripcio = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Recurs Name',
                    }),
                    required=False)
    url = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'URL',
                    }),
                    required=False)
    etiquetes =  autocomplete_light.MultipleChoiceField('EtiquetaAutocomplete')

    adjunt = forms.FileField()



    def __init__(self, *args, **kwargs):
        super(RecursForm, self).__init__(*args, **kwargs)
        self.fields['etiquetes'].required = False
        self.fields['descripcio'].required = False
        self.fields['adjunt'] = forms.FileField(u'imagen', widget=forms.ClearableFileInput(attrs={'class':'btn btn-md btn-primary'}))
        self.fields['adjunt'].required = False
