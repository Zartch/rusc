from django import forms
from .models import Etiqueta, Tesauro
import autocomplete_light

autocomplete_light.register(Etiqueta, search_fields=('nom', ))


class etiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        exclude = {"tipologia"}




class tesauroForm(forms.ModelForm):

    class Meta:
        model = Tesauro
        exclude = {}
        widgets = {}