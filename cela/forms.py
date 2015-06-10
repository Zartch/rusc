from django import forms
from cela.models import Cela
from django.contrib.auth.models import User
import autocomplete_light
from post.models import Post

autocomplete_light.register(User, search_fields=('username', ))

class celaForm(forms.ModelForm):

    class Meta:
        model = Cela
        exclude = {}

    widgets = {
        	'moderadors': autocomplete_light.MultipleChoiceWidget('UserAutocomplete'),}


class modeform(forms.Form):


    class Meta:
        model = Post
        fields = ['titol','text']