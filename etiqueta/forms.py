from django import forms
from .models import Etiqueta

class etiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        exclude = {"tipologia"}


