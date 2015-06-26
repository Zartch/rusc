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

    def __init__(self, *args, **kwargs):
        super(celaForm, self).__init__(*args, **kwargs)
        self.fields['descripcio'].widget.attrs.update({'class' : 'form-control'})
        self.fields['tipus'].widget.attrs.update({'class' : 'form-control'})
        self.fields['pregunta'].widget.attrs.update({'class' : 'form-control'})
        # self.fields['moderadors'].widget.attrs.update({'class' : 'form-control'})



class modeform(forms.Form):

    class Meta:
        model = Post
        fields = ['titol','text']