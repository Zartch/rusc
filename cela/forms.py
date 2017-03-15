# -*- coding: utf-8 -*-
from django import forms

from cela.models import Cela
#Form para la creación de la Red
class celaForm(forms.ModelForm):

    class Meta:
        model = Cela
        exclude = {'slug', 'moderadors','personal'}
        #widgets = {'moderadors': autocomplete_light.MultipleChoiceWidget('UserAutocomplete'),}

    def __init__(self, *args, **kwargs):
        super(celaForm, self).__init__(*args, **kwargs)
        self.fields['descripcio'].widget.attrs.update({'class' : 'form-control'})
        self.fields['tipus'].widget.attrs.update({'class' : 'form-control'})
        self.fields['pregunta'].widget.attrs.update({'class' : 'form-control'})
        #self.fields['moderadors'].widget.attrs.update({'class' : 'form-control'})
        self.fields['dato_veri'].widget.attrs.update({'class' : 'form-control'})
        self.fields['temas'].widget.attrs.update({'class' : 'form-control'})

    def clean(self):
        #Los temas se crearán despúes, no se tiene que validar.
        super(celaForm, self).clean() #if necessary
        if 'temas' in self._errors:
            del self._errors['temas']


#Form para la modificación de la Red
class celaModForm(forms.ModelForm):

    class Meta:
        model = Cela
        exclude = {'slug'}
        #widgets = {'moderadors': autocomplete_light.MultipleChoiceWidget('UserAutocomplete'),}

    def __init__(self, *args, **kwargs):
        super(celaModForm, self).__init__(*args, **kwargs)
        self.fields['descripcio'].widget.attrs.update({'class' : 'form-control'})
        self.fields['tipus'].widget.attrs.update({'class' : 'form-control'})
        self.fields['pregunta'].widget.attrs.update({'class' : 'form-control'})
        #self.fields['moderadors'].widget.attrs.update({'class' : 'form-control'})
        self.fields['dato_veri'].widget.attrs.update({'class' : 'form-control'})
        self.fields['temas'].widget.attrs.update({'class' : 'form-control'})
        self.fields['moderadors'].widget.attrs.update({'class' : 'form-control'})
        self.fields['personal'].widget.attrs.update({'class' : 'form-control'})

    def clean(self):
        #Los temas se crearán despúes, no se tiene que validar.
        super(celaModForm, self).clean() #if necessary
        if 'temas' in self._errors:
            del self._errors['temas']


class celaInitialInfo(forms.ModelForm):

    class Meta:
        model = Cela
        fields = ['personal']



#Form para substituir el form de registro y añadirle el captcha
from captcha.fields import ReCaptchaField
class AllauthSignupForm(forms.Form):

    captcha = ReCaptchaField()
    def signup(self, request, user):
        """ Required, or else it throws deprecation warnings """
        pass
