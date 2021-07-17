from django import forms
from django.contrib.auth.models import User
from .models import *


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    class Meta:
        model=User
        fields=('username','email','password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )




CATEGORY_CHOICES = (
    ('food','FOOD'),
    ('technical','TECHNICAL'),
    ('technology','TECHNOLOGY'),
    ('news','NEWS'),
    ('movies','MOVIES'),
    ('history','HISTORY'),
    ('knowledge','KNOWLEDGE'),
    ('fitness','FITNESS'),
    ('games','GAMES'),
    ('social','SOCIAL'),
    ('economy','ECONOMY'),
    ('business','BUSINESS'),
    ('others','OTHERS'),
)

class PreferenceForm(forms.ModelForm):
    # Category =  forms.CharField(widget=forms.CheckboxSelectMultiple(choices=CATEGORY_CHOICES))
    class Meta:
        model=Preference
        fields = '__all__'