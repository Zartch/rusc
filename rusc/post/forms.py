# -*- coding: utf-8 -*-
from django import forms
from rusc.post.models import Post,Vote
from cela.models import get_cela
from rusc.etiqueta.models import Etiqueta


class postForm(forms.ModelForm):

    etiquetes = forms.ModelChoiceField(queryset="", initial="")

    class Meta:
        model = Post
        exclude = {"autor", "pare", "recursos", "moderacio", "cela", "rank_score", "num_comments"}
        widgets = {}


    def clean(self):
        super(postForm, self).clean() #if necessary
        if 'etiquetes' in self._errors:
            del self._errors['etiquetes']

    def __init__(self, *args,**kwargs):
        try:
            self.request = kwargs.pop('request')
        except:
            pass
        super (postForm,self ).__init__(*args,**kwargs)
        self.fields['titol'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['class'] = 'form-control id_text'
        self.fields['etiquetes'].widget.attrs['class'] = 'form-control'
        self.fields['etiquetes'].widget.attrs['class'] = 'etiquetes'
        self.fields['etiquetes'].widget.attrs['style'] = 'width: 100%'
        self.fields['etiquetes'].widget.attrs['multiple'] = 'multiple'
        try:
            self.fields['etiquetes'].queryset = Etiqueta.objects.filter(cela= get_cela(self.request))
        except:
            self.fields['etiquetes'].queryset = Etiqueta.objects.all()

class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = '__all__'



