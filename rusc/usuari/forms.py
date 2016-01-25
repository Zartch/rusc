# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from rusc.etiqueta.models import Etiqueta
from cela.models import get_cela
from rusc.usuari.models import UserProfile, UserInfo


class userProfileForm(forms.ModelForm):


    website = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': "form-control"}),
        required=False,
    )

    tipusSubscripcio = forms.ChoiceField(choices=UserProfile.TIPUS_SUBSCRIPCIO,widget=forms.Select(attrs={'class':'form-control'}))
    mailConf = forms.ChoiceField(choices=UserProfile.ENVIAMENT_MAIL, widget=forms.Select(attrs={'class':'form-control'}))
    # querrySet = Post.objects.filter().values_list("pk","titol")
    # subscripcions = forms.MultipleChoiceField(choices= querrySet,widget=forms.SelectMultiple(attrs={'class':'form-control'}))

    def clean(self):
        super(userProfileForm, self).clean() #if necessary
        if 'mailConf' in self._errors:
            del self._errors['mailConf']

    class Meta:
        model = UserProfile
        exclude = {"cela", "user", "estat","email_p"}
        fields = ("avatar","website","tipusSubscripcio","mailConf","subscripcions")

        labels = {
            'mailConf' : _('Correu electronic'),
            'tipusSubscripcio' : _('Tipus subscripcio'),
            'website': _('WEB'),
        }

        help_text= {
            'tipusSubscripcio' : 'A dis de la cela'
        }

    def __init__(self, *args, **kwargs):
        super(userProfileForm, self).__init__(*args, **kwargs)
        self.fields['avatar'] = forms.ImageField(u'imagen', widget=forms.ClearableFileInput(attrs={'class':'btn btn-md btn-primary'}))
        self.fields['avatar'].required = False
        self.fields['subscripcions'].widget.attrs['class'] = 'vSelectMultipleField form-control'


class userProfileGeneralForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = {"cela", "user", "estat","subscripcions","email_p","website", "etiquetes"}

import django_select2
class userInfoForm(forms.Form):
    etq = forms.ChoiceField(widget=forms.Select(attrs={'class':'regDropDown'}))
    visible = forms.BooleanField(initial=True)
    #home = forms.BooleanField(initial=False)

    chivato = 0
    class Meta:
        model = UserInfo
        exclude = {"usr"}
    #el request y el selected los pasamos cuando insatnciamos el form
    def __init__(self, request, selected, *args, **kwargs):
        super(userInfoForm, self).__init__(*args, **kwargs)
        #self.fields['etq'].widget.attrs['class'] = 'form-control'
        try:
            cho = []
            cho.append(['',''])
            for etq in Etiqueta.objects.filter(cela= get_cela(request)):
                cho.append([etq.pk,etq.nom])
            self.fields['etq'] = forms.ChoiceField(choices= cho)
            self.fields['etq'].widget.attrs['class'] = 'etiquetes'
            self.initial['etq'] = ''
            #selected es un array que nos dirá el estado
            if len(selected) > 0:
                self.initial['etq'] = selected[-1][0]
                self.initial['visible'] = selected[-1][1]
                selected.pop()

        except  Exception as e:
            self.fields['etq'] = forms.ChoiceField(choices=[[1,1],[2,2],[3,3] ])




