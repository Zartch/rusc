from django import forms
from usuari.models import UserProfile
from post.models import Post
from cela.models import get_cela

class userProfileForm(forms.ModelForm):

    # def __init__(self, user, *args, **kwargs):
    #         super(userProfileForm, self).__init__(*args, **kwargs)
    #         self.fields['subscripcions'].queryset = Post.objects.all()

    avatar = forms.FileField()
    website = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': "form-control"}),
    )

    tipusSubscripcio = forms.ChoiceField(choices=UserProfile.TIPUS_SUBSCRIPCIO,widget=forms.Select(attrs={'class':'form-control'}))
    mailConf = forms.ChoiceField(choices=UserProfile.ESTAT_SUBSCRIPCIO, widget=forms.Select(attrs={'class':'form-control'}))
    qs = [["Value1","name1"],["Value2","Name2"]]
    querrySet = Post.objects.filter().values_list("pk","titol")
    #[a.append(s) for a in ]
    subscripcions = forms.MultipleChoiceField( choices= querrySet,widget=forms.SelectMultiple(attrs={'class':'form-control'}))

    class Meta:
        model = UserProfile
        exclude = {"cela", "user", "estat","email_p"}
        # widgets = {
        #     #'subscripcions': forms.MultiWidget(attrs={'class': "form-control"}),
        #     #'subscripcions': forms.MultiWidget(attrs={'class': "form-control"}),
        # }




class userProfileGeneralForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = {"cela", "user", "estat","subscripcions","email_p","website"}