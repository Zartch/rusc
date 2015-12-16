# -*- coding: utf-8 -*-
from django import forms
from django.utils.datastructures import MultiValueDictKeyError

from rusc.etiqueta.models import Etiqueta
from cela.models import get_cela


class RecursForm(forms.Form):
    """
    Form for individual user links
    """
    descripcio = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Recurs Name',
                    }),
                    required=True)
    url = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'URL',
                    }),
                    required=False)
    #etiquetes =  autocomplete_light.MultipleChoiceField('EtiquetaAutocomplete')
    etiquetes = forms.ModelChoiceField(queryset="", initial="")
    adjunt = forms.FileField()


    def clean(self):
        super(RecursForm, self).clean() #if necessary
        if 'etiquetes' in self._errors:
            del self._errors['etiquetes']
        try:
            if self.data['url']=='' and  self.data['adjunt']=='':
                self._errors['url'] = ["Es necesari un adjunt o una URL"]
                self._errors['adjunt'] = ["Es necesari un adjunt o una URL"]
        except MultiValueDictKeyError:
            pass
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        try:
            self.request = kwargs.pop('request')
        except:
            pass
        super(RecursForm, self).__init__(*args, **kwargs)
        self.fields['etiquetes'].required = False
        self.fields['descripcio'].required = False
        self.fields['url'].widget.attrs['class'] = 'form-control'
        self.fields['descripcio'].widget.attrs['class'] = 'form-control'
        self.fields['adjunt'] = forms.FileField(u'imagen', widget=forms.ClearableFileInput(attrs={'class':'btn btn-md btn-primary'}))
        self.fields['adjunt'].required = False
        try:
            self.fields['etiquetes'].queryset = Etiqueta.objects.filter(cela= get_cela(self.request))
        except:
            pass
        self.fields['etiquetes'].widget.attrs['class'] = 'etiquetes'
        self.fields['etiquetes'].widget.attrs['style'] = 'width: 100%'
        self.fields['etiquetes'].widget.attrs['multiple'] = 'multiple'