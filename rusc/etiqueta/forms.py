# -*- coding: utf-8 -*-
from django import forms


from rusc.etiqueta.models import Etiqueta, Tesauro
from cela.models import get_cela



class etiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        exclude = {"tipologia"}

class newEtiquetaForm(forms.ModelForm):

    class Meta:
        model = Etiqueta
        exclude = {"slug", "datahora", "relacio","cela","ficha"}
        widgets = {}

    def __init__(self, instance, *args, **kwargs):
            self.request = kwargs.pop('request')
            super(newEtiquetaForm, self).__init__(*args, **kwargs)
            #cela = forms.ch(widget=forms.HiddenInput(), initial=123)
            # self.fields['etiquetes'].required = False
            # self.fields['etiquetes'].queryset = Etiqueta.objects.filter(cela= get_cela(self.request))
            # self.fields['etiquetes'].widget.attrs['class'] = 'etiquetes'
            # self.fields['etiquetes'].widget.attrs['style'] = 'width: 100%'
            # self.fields['etiquetes'].widget.attrs['multiple'] = 'multiple'



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



