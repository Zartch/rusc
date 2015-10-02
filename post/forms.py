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


class VoteForm(forms.ModelForm):

    class Meta:
        model = Vote
        fields = '__all__'



