from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CHOICES = [('Pub', 'Public'), ('Pri', 'Private')]

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


class Task(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=2000000, default=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,default="")
    Category = models.CharField(max_length=11, choices=CATEGORY_CHOICES, default='select')
    VisibilityMode = models.CharField(choices=CHOICES, max_length=128, default='Pub')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
