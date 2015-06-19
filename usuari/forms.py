from django import forms
from usuari.models import UserProfile


class userProfileForm(forms.ModelForm):

    avatar = forms.FileField()
    website = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': "form-control"}),
    )


    class Meta:
        model = UserProfile
        exclude = {"cela", "user", "estat"}




class userProfileGeneralForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = {"cela", "user", "estat","subscripcions","email_p","website"}