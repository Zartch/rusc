from django import forms
from .models import Etiqueta, Tesauro
from cela.models import get_cela
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


    def __init__(self, *args,**kwargs):
        self.request = kwargs.pop('request')
        super (tesauroForm,self ).__init__(*args,**kwargs)
        self.fields['etq1'].queryset = Etiqueta.objects.filter(cela= get_cela(self.request))
        self.fields['etq2'].queryset = Etiqueta.objects.filter(cela= get_cela(self.request))
        self.fields['etq1'].widget.attrs['style'] = 'width: 100%'
        self.fields['etq2'].widget.attrs['style'] = 'width: 100%'
        self.fields['etq1'].widget.attrs['class'] = 'id_etq1'
        self.fields['etq2'].widget.attrs['class'] = 'id_etq2'
        self.fields['tipo'].widget.attrs['class'] = 'form-control'

