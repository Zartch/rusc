from django import forms
from post.models import Post,Vote
import autocomplete_light
from etiqueta.models import Etiqueta

autocomplete_light.register(Etiqueta, search_fields=('nom', ))

class postForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = {"autor", "pare","recursos","moderacio", "cela"}
        widgets = {
        	'etiquetes': autocomplete_light.MultipleChoiceWidget('EtiquetaAutocomplete'),}

    def __init__(self, *args,**kwargs):
        super (postForm,self ).__init__(*args,**kwargs)
        self.fields['titol'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['class'] = 'form-control'
        self.fields['etiquetes'].widget.attrs['class'] = 'form-control'


class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = '__all__'



