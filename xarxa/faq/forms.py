# -*- coding: utf-8 -*-
from django import forms

from xarxa.faq.models import Pregunta


class faqForm(forms.ModelForm):

    class Meta:
        model = Pregunta
        exclude = {'created_on','updated_on','created_by','updated_by','cela'}

    def __init__(self, *args, **kwargs):
        super(faqForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class' : 'form-control'})
        self.fields['answer'].widget.attrs.update({'class' : 'form-control'})
        self.fields['sort_order'].widget.attrs.update({'class' : 'form-control'})
