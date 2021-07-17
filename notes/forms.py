from django import forms
from django.forms import ModelForm

from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add new title...'}))
    desc = forms.CharField(widget=forms.TextInput(attrs={'id':'foo','placeholder': 'Add Description...'}))
    CATEGORY_CHOICES = (
        ('food', 'FOOD'),
        ('technical', 'TECHNICAL'),
        ('technology', 'TECHNOLOGY'),
        ('news', 'NEWS'),
        ('movies', 'MOVIES'),
        ('history', 'HISTORY'),
        ('knowledge', 'KNOWLEDGE'),
        ('fitness', 'FITNESS'),
        ('games', 'GAMES'),
        ('social', 'SOCIAL'),
        ('economy', 'ECONOMY'),
        ('business', 'BUSINESS'),
        ('others', 'OTHERS'),
    )

    Category = forms.CharField(label='Category',widget=forms.Select(attrs={'id': 'chId'}, choices=CATEGORY_CHOICES), required=True)
    CHOICES = [('Pub', 'Public'), ('Pri', 'Private')]
    VisibilityMode = forms.CharField(label='Visibility Mode', widget=forms.RadioSelect(attrs={'id' : 'myId'},choices=CHOICES), required=True)

    class Meta:
        model = Task
        fields = '__all__'
        required = (
            'title',
            'desc',
            'Category',
            'VisibilityMode',
        )

