# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
import autocomplete_light

from cela.models import Cela


autocomplete_light.register(User, search_fields=('username', ))

class celaForm(forms.ModelForm):

    class Meta:
        model = Cela
        exclude = {'slug', 'moderadors'}
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

from captcha.fields import ReCaptchaField

class AllauthSignupForm(forms.Form):

    captcha = ReCaptchaField()

    def signup(self, request, user):
        """ Required, or else it throws deprecation warnings """
        pass
