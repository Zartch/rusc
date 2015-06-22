from django import forms
import autocomplete_light
from etiqueta.models import Etiqueta

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

