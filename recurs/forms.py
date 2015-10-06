from django import forms
from etiqueta.models import Etiqueta
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
        if self.data['adjunt']=="" and  self.data['url']== "":
            self._errors['url'] = ["Es necesari un adjunt o una URL"]
            self._errors['adjunt'] = ["Es necesari un adjunt o una URL"]
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RecursForm, self).__init__(*args, **kwargs)
        self.fields['etiquetes'].required = False
        self.fields['descripcio'].required = False
        self.fields['url'].widget.attrs['class'] = 'form-control'
        self.fields['descripcio'].widget.attrs['class'] = 'form-control'
        self.fields['adjunt'] = forms.FileField(u'imagen', widget=forms.ClearableFileInput(attrs={'class':'btn btn-md btn-primary'}))
        self.fields['adjunt'].required = False
        self.fields['etiquetes'].queryset = Etiqueta.objects.filter(cela= get_cela(self.request))
        self.fields['etiquetes'].widget.attrs['class'] = 'etiquetes'
        self.fields['etiquetes'].widget.attrs['style'] = 'width: 100%'
        self.fields['etiquetes'].widget.attrs['multiple'] = 'multiple'