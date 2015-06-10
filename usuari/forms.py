__author__ = 'Zartch'
#http://johnparsons.net/index.php/2013/06/28/creating-profiles-with-django-registration/
from registration.forms import RegistrationForm
from django import forms

class ExRegistrationForm(RegistrationForm):
    website = forms.CharField(label='Your website', max_length=100)
    #avatar = forms.ImageField()