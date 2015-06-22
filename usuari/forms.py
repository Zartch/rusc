from django import forms
from usuari.models import UserProfile
from post.models import Post
from cela.models import get_cela

class userProfileForm(forms.ModelForm):



    avatar = forms.FileField(required=False)
    website = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': "form-control"}),
        required=False,
    )

    tipusSubscripcio = forms.ChoiceField(choices=UserProfile.TIPUS_SUBSCRIPCIO,widget=forms.Select(attrs={'class':'form-control'}))
    mailConf = forms.ChoiceField(choices=UserProfile.ENVIAMENT_MAIL, widget=forms.Select(attrs={'class':'form-control'}))
    querrySet = Post.objects.filter().values_list("pk","titol")
    subscripcions = forms.MultipleChoiceField(choices= querrySet,widget=forms.SelectMultiple(attrs={'class':'form-control'}))

    class Meta:
        model = UserProfile
        exclude = {"cela", "user", "estat","email_p"}

    def __init__(self, *args, **kwargs):
        super(userProfileForm, self).__init__(*args, **kwargs)
        self.fields['avatar'] = forms.ImageField(u'imagen', widget=forms.ClearableFileInput(attrs={'class':'btn btn-md btn-primary'}))



class userProfileGeneralForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = {"cela", "user", "estat","subscripcions","email_p","website"}