__author__ = 'zartch'
from django import forms

from xarxa.etiqueta.models import Ficha


class fichaForm(forms.ModelForm):

    class Meta:
        model = Ficha
        exclude = {'etq'}

    def __init__(self, request,*args, **kwargs):
        super(fichaForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs['class'] = 'form-control'
        self.fields['descrip'].widget.attrs['class'] = 'form-control'
        self.fields['obliatorio'].widget.attrs['class'] = 'form-control'
        self.fields['hint'].widget.attrs['class'] = 'form-control'